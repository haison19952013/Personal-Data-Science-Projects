import pandas as pd
import os
from job_tools import job_scraper

def get_response(user_input: str) -> list:
    responses = []
    include_tags = []
    exclude_tags = []
    command: str = user_input.lower()
    split_command = command.split()
    if split_command[1] == 'show-jobs':
        responses.append(f'Subcommand {split_command[1]} is used.')
        if '--new' in split_command:
            scrape_new_jobs()
            responses.append('Getting new job opportunities.')
        if '--n' in split_command:
            try:
                n = int(split_command[split_command.index('--n') + 1])
                responses.append(f'Getting first {n} job opportunities.')
            except Exception as e:
                responses.append(f'An error occurred while getting the number of job: {e}')
                responses.append('Default number of job opportunities is set to 5.')
                n = 5
        if '--include' in split_command:
            try:
                include_tags = split_command[split_command.index('--include') + 1].split('-')
                responses.append(f'Including tags {include_tags} in the job opportunities.')
            except Exception as e:
                responses.append(f"An error occurred while including the job: {e}")
        if '--exclude' in split_command:
            try:
                exclude_tags = split_command[split_command.index('--exclude') + 1].split('-')
                responses.append(f'Excluding tags {exclude_tags} from the job opportunities.')
            except Exception as e:
                responses.append(f'An error occurred while excluding the job: {e}')
        df = reload_jobs(include_tags = include_tags, exclude_tags = exclude_tags)
        print(df)
        return get_csv_rows(responses = responses , df = df, num_rows = n)
    else:
        return ['Invalid commands']

def scrape_new_jobs():
    obj = job_scraper()
    obj.scrape(total_page = 1)
    obj.to_datalake()

def reload_jobs(include_tags: list, exclude_tags: list):
    if len(os.listdir('data_lakehouse')) == 0: 
        return "No existing database. Please add argument --new to your command to scrape new jobs"
    file_name = os.listdir('data_lakehouse')[-1] # Get the lastest file in the data lakehouse
    file_path = os.path.join('data_lakehouse', file_name)
    obj = job_scraper()
    obj.load_datalake(file_path = file_path)
    if len(include_tags) == 0 and len(exclude_tags) == 0:
        return obj.data_frame
    else:
        return obj.to_datawarehouse(include_tags = include_tags, exclude_tags = exclude_tags, no_save = True)

def get_csv_rows(responses:list , df: pd.DataFrame, num_rows: int = 5) -> list:
    """
    Reads the first few rows from a CSV file using pandas and formats them into a string.
    Splits the response into chunks to ensure no message exceeds 2000 characters.
    :param file_path: Path to the CSV file.
    :param num_rows: Number of rows to display.
    :return: List of formatted strings, each under 2000 characters.
    """

    try:        
        # Select the first 'num_rows' rows
        df = df[['job link','job title','company name','location','work type','posted time']].head(num_rows)
        df.sort_values('posted time', ascending = False, inplace = True)

        # Convert the dataframe to a formatted string
        current_message = ""

        for _, row in df.iterrows():
            formatted_row = '\n'.join([f"{col}: {row[col]}" for col in df.columns])
            formatted_row += f"\n{'-'*20}\n"

            if len(current_message) + len(formatted_row) > 2000:
                responses.append(current_message)
                current_message = formatted_row
            else:
                current_message += formatted_row

        # Add any remaining content
        if current_message:
            responses.append(current_message)

        return responses

    except Exception as e:
        return [f'Error reading CSV file: {str(e)}']

# if __name__ == '__main__':
#     print(get_response('!discord-bot show-jobs --new --n 20 --include python-java -exclude internship'))