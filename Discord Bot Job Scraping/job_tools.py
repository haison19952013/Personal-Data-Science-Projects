# %%
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import os
from functools import wraps
# %%
def chrome_driver_operation(retries: int = 3) -> callable:
    """
    Decorator for ChromeDriver operations with retries. The decorator will retry the operation for the given number of times if it fails.
    
    Args:
        retries (int): The number of times to retry the operation. Default is 3.
    
    Return:
        A decorator function that wraps the original function.
    """

    assert type(retries) == int, "Number of retries must be an integer"
    assert retries > 0, "Number of retries must be greater than 0"

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # Get the 'self' from the instance method
            for i in range(retries):
                print(f'Perform {func.__name__}: attempt {i+1}...')
                try:
                    with webdriver.Chrome() as driver:
                        result = func(self, driver, *args[1:], **kwargs)
                        if isinstance(result, dict):
                            if not any([val is np.nan for val in result.values()]):
                                return result
                            else:
                                print(f"Perform {func.__name__}: attempt {
                                      i+1} failed, retrying...")
                        else:
                            if result is not None:
                                return result
                            else:
                                print(f"Perform {func.__name__}: attempt {
                                      i+1} failed, retrying...")
                except Exception as e:
                    print(f"Perform {func.__name__}: attempt {
                          i+1} failed with error: {e}")
        return wrapper
    return decorator


class job_scraper(object):
    """This class scrapes job details from a website and stores the data in a pandas DataFrame.
    
    Attributes:
        data_frame (pd.DataFrame): The pandas DataFrame that stores the scraped job details.
        data_list (list): The list that stores the scraped job details in dictionary format.
    """

    def __init__(self):
        self.data_frame = None
        self.data_list = []

    def scrape(self, total_page: int = 1) -> None:
        """
        Scrape job details from the website and store them in the pandas DataFrame.
        
        Args:
            - total_page (int): The total number of pages to scrape. Default is 1.

        Return:
            - None
        """

        self.get_max_page()
        for page_num in range(1, total_page + 1):
            print("Scraping page: ", page_num)
            self.scrape_single_page(page_num=page_num)
            print("Scraping page: ", page_num, "completed")
            time.sleep(5)
        self.to_datalake()
        print("Scraping completed")

    def scrape_single_page(self, page_num: int = 1) -> None:
        """
        Scrape job details from a single page of the website and store them in the data_list.
        
        Args:
            - page_num (int): The page number to scrape. Default is 1.

        Return:
            - None
        """
        data_list = []
        self.update_job_url(data_list=data_list,  page_num=page_num)
        assert len(data_list) > 0, "No job links are found"
        for data_dict in data_list:
            if len(self.data_list) > 0:
                if data_dict["job link"] in [x['job link'] for x in self.data_list]:
                    continue
            print(data_dict['job link'])
            self.update_job_detail(data_dict=data_dict)
        self.data_list += data_list

    def to_datalake(self) -> None:
        """
        Save the scraped job details in a pandas DataFrame to a CSV file.
        The DataFrame includes columns: job title, company name, job location, job description, job link, and posted time.
        """
        self.data_frame = pd.DataFrame(self.data_list)
        self.data_frame['posted time'] = pd.to_datetime(
            self.data_frame['posted time'])
        print(self.data_frame.info())
        full_name = f'{datetime.now().strftime('%Y%m%dT%H%M%S')}{
            'itviec_lakehouse'}.csv'
        save_folder_path = os.path.join(os.getcwd(), 'data_lakehouse')
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
        file_path = os.path.join(save_folder_path, full_name)
        self.data_frame.to_csv(file_path, index=False)
        print(
            f"##### Save the data successfully to './data_lakehouse/{full_name}' #####")

    def to_datawarehouse(self, include_tags: str | list, exclude_tags: str | list, no_save: bool = False) -> None | pd.DataFrame:
        """
        Filter and save the scraped job details in a pandas DataFrame to a CSV file based on the given tags.
        The DataFrame includes columns: job title, company name, job location, job description, job link, and posted time.

        Args:
            - include_tags (str or list): The keyword(s) to include in the job details. Default is None.
            - exclude_tags (str or list): The keyword(s) to exclude in the job details. Default is None.
            - no_save (bool): Whether to save the filtered data to a CSV file. Default is False.
        
        Return:
            - None | pd.DataFrame: The filtered DataFrame if no_save is True.
        """
        assert self.data_frame is not pd.DataFrame, "Data is not reloaded as a DataFrame from data lake house"
        if isinstance(include_tags, str):
            include_tags = [include_tags]
        if isinstance(exclude_tags, str):
            exclude_tags = [exclude_tags]

        filtered_df = self.data_frame.copy()
        filtered_columns = filtered_df.drop(['job link', 'posted time'], axis=1).columns
        for col in filtered_columns:
            filtered_df[col] = filtered_df[col].str.lower()
        # convert to lower case for case-insensitive
        if len(include_tags) != 0:
            include_tags = [keyword.lower() for keyword in include_tags]
            for idx, col in enumerate(filtered_columns):
                if idx == 0:
                    include_condition = filtered_df[col].str.contains(
                        '|'.join(include_tags))
                else:
                    include_condition = include_condition | filtered_df[col].str.contains(
                        '|'.join(include_tags))
            filtered_df = filtered_df[include_condition]           
        # convert to lower case for case-insensitive
        if len(exclude_tags) != 0:
            exclude_tags = [keyword.lower() for keyword in exclude_tags]
            for idx, col in enumerate(filtered_columns):
                if idx == 0:
                    exclude_condition = filtered_df[col].str.contains(
                        '|'.join(exclude_tags))
                else:
                    exclude_condition = exclude_condition | filtered_df[col].str.contains(
                        '|'.join(exclude_tags))
            exclude_condition = ~exclude_condition
            filtered_df = filtered_df[exclude_condition]

        if no_save:
            return filtered_df
        else:
            full_name = f'{'itviec_datawarehouse'}_include_{
                '_'.join(include_tags)}_exclude_{'_'.join(exclude_tags)}.csv'
            save_folder_path = os.path.join(os.getcwd(), 'data_warehouse')
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)
            file_path = os.path.join(save_folder_path, full_name)
            filtered_df.to_csv(file_path, index=False)
            print(
                f"##### Save the data successfully to './data_warehouse/{full_name}' #####")


    def load_datalake(self, file_path: str) -> None:
        """
        Load the scraped job details from a CSV file into the pandas DataFrame.

        Args:
            - file_path (str): The path of the CSV file to load.
        
        Return:
            - None
        """

        assert os.path.exists(file_path), "File path does not exist"
        self.data_frame = pd.read_csv(file_path, parse_dates=['posted time'])
        print(self.data_frame.info())
        print(f"##### Load the data successfully from '{file_path}' #####")

    @chrome_driver_operation(retries=3)
    def get_max_page(self, driver) -> int:
        """
        Fetch the maximum page number from the website.

        Args:
        - driver (WebDriver): The initialized Chrome WebDriver object.
        
        Return:
        - int: The maximum page number.
        """
        assert driver is not None, "Driver object is not initialized"
        url = 'https://itviec.com/it-jobs?job_selected=senior-expert-backend-engineer-javascript-nodejs-smg-swiss-marketplace-group-2726&page=1'
        driver.get(url)
        try:
            # Wait for the pagination elements to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "page"))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_page_obj = soup.find_all('div', class_="page")
            max_page_obj = [page for page in all_page_obj if len(
                page.get('class')) == 1][-1]
            self.max_page = int(max_page_obj.find('a').get_text())
            return int(max_page_obj.find('a').get_text())
        except Exception as e:
            print(f"An error occurred while fetching the max page: {e}")

    @chrome_driver_operation(retries=3)
    def update_job_url(self, driver, data_list: list, page_num: int = 1) -> list:
        """
        Update the job URLs in the given data list for the given page number.

        Args:
        - driver (WebDriver): The initialized Chrome WebDriver object.
        - data_list (list): The list of job details (dict) to update.
        - page_num (int, optional): The page number for which to update job URLs. Defaults to 1.

        Return:
        - data_list (list): The updated data list (dict) with job URLs.
        """

        # Assert the arguments
        assert driver is not None, "Driver object is not initialized"
        assert type(data_list) == list, "data_list should be a list"
        assert type(page_num) == int, "page_num should be a positive integer"
        assert page_num > 0, "page_num should be a positive integer"
        assert page_num <= self.max_page, f"Page number {
            page_num} exceeds the maximum page number {self.max_page}"

        # Update job URLs for the given page number
        url = f'https://itviec.com/it-jobs?job_selected=senior-expert-backend-engineer-javascript-nodejs-smg-swiss-marketplace-group-2726&page={
            page_num}'
        driver.get(url)

        try:
            # Explicit wait for the job listings container to ensure the page is loaded
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.ipx-4.ipx-md-3'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_obj_list = soup.find_all('div', class_='ipx-4 ipx-md-3')

            for job_obj in job_obj_list:
                job_url_raw = job_obj.find(
                    'div', class_='ipy-2').find('h3', class_='imt-3').find('a')['href'].split('?')[0]
                data_list.append(
                    {'job link': 'https://itviec.com' + job_url_raw})
            return data_list

        except Exception as e:
            print(f"An error occurred while updating job URLs for page {
                  page_num}: {e}")

    @chrome_driver_operation(retries=3)
    def update_job_detail(self, driver, data_dict: dict) -> dict:
        """
        Update the job details for the given job link.

        Args:
        - driver (WebDriver): The initialized Chrome WebDriver object.
        - data_dict (dict): The dictionary containing job details (dict) to update.
        
        Return:
        - data_dict (dict): The updated dictionary containing job details (dict).

        """
        # Assert the arguments
        assert driver is not None, "driver object is not initialized"
        assert type(data_dict) == dict, "data_dict should be a dictionary"
        # Update job details for the given job links
        driver.get(data_dict['job link'])
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.job-header-info h1.ipt-md-6.text-it-black'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time_now = datetime.now()

            job_title = soup.find('div', class_='job-header-info').find(
                'h1', class_='ipt-md-6 text-it-black').get_text(strip=True)
            company_name = soup.find(
                'div', class_='job-header-info').find('div', class_='employer-name').get_text(strip=True)
            location = soup.find('div', class_='d-inline-block text-dark-grey').find(
                'span', class_='normal-text text-rich-grey').get_text(strip=True)
            jd = soup.find_all('div', class_='imy-5 paragraph')[0].get_text()
            requirement = soup.find_all(
                'div', class_='imy-5 paragraph')[1].get_text()
            work_type = soup.find(
                'span', class_='normal-text text-rich-grey ms-1').get_text()
            posted_time_src = soup.find_all(
                'span', class_='normal-text text-rich-grey')
            for src in posted_time_src:
                if 'Posted' in src.get_text(strip=True):
                    number = float(src.get_text(strip=True).split()[1])
                    unit = src.get_text(strip=True).split()[2]
                    if unit in ['hours', 'hour']:
                        posted_time = (
                            time_now - timedelta(hours=number)).strftime('%Y-%m-%d %H:%M:%S')
                    elif unit in ['minutes', 'minute']:
                        posted_time = (
                            time_now - timedelta(minutes=number)).strftime('%Y-%m-%d %H:%M:%S')

            data_dict['job title'] = job_title
            data_dict['company name'] = company_name
            data_dict['location'] = location
            data_dict['work type'] = work_type
            data_dict['jd'] = jd
            data_dict['requirement'] = requirement
            data_dict['posted time'] = posted_time
            return data_dict

        except Exception as e:
            print(f"An error occurred while updating job details from {
                  data_dict['job link']}: {e}")

# %%
if __name__ == '__main__':
    # Test 1: scrape new data
    obj = job_scraper()
    obj.scrape(total_page = 2)
    obj.to_datawarehouse(include_tags = ['Python'], exclude_tags = ['remote'])

    #Test 2: reload existing data
    assert len(os.listdir('data_lakehouse')) > 0, "Please perform Test 1 first to create the data lakehouse"
    file_name = os.listdir('data_lakehouse')[-1] # Get the lastest file in the data lakehouse
    file_path = os.path.join('data_lakehouse', file_name)
    obj2 = job_scraper()
    obj2.load_datalake(file_path = file_path)
    obj2.to_datawarehouse(include_tags = ['Python'], exclude_tags = ['remote'])

