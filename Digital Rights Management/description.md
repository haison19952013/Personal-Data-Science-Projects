# The Challenge
Effective management of digital rights management (DRM) keys is crucial for FPT Television, as it directly impacts business costs and budgeting. However, the lack of a comprehensive BI Dashboard or regular reports has hindered the ability to track and forecast DRM key usage accurately. To address this challenge, s95bet.com Joint Stock Company for Digital Transformation Services has developed this report, providing precise insights into the current key granting situation and forecasting future trends.

# What Data Will I Use in This Project?
Data link: [DRM Key Usage Data](https://drive.google.com/drive/folders/1ViaNctgS91Xre_tGXkwqG_fuOswfs1CO?usp=sharing)

In this project, the data is stored in five tables: 
1. Log_BHD_Movieid (FACT): Contains customer ID and movie ID from BHD company
2. Log_FimPlus_Movieid (FACT): Contains customer ID and movie ID from Fimplus company
3. Log_Get_DRM_list (FACT): Contains customer ID and movie ID from FimGoi group
4. Customer (DIM): Contains information of customers such as customers ID, MAC address and the account created date
5. CustomerService (DIM): Contains information of customers that pays for using products of FimGoi
6. MV_PropertiesShowVN (DIM): Contains the movie ID and the bool value to check whether the products requiring DRM keys from BHD and Fimplus or not

# Data Dictionary
Table: MV_PropertiesShowVN (DIM)
| Column Name | Type    |
|-------------|---------|
| id (PK)     | int     |
| isDRM       | bool    |

Table: Log_BHD_Movieid (FACT)
| Column Name      | Type    |
|------------------|---------|
| CustomerID (PK)  | int     |
| MovieID (FK)     | int     |

Table: Log_FimPlus_Movieid (FACT)
| Column Name     | Type |
|-----------------|------|
| CustomerID (PK) | int  |
| MovieID (FK)    | int  |

Table: Log_Get_DRM_list (FACT)
| Column Name     | Type      |
|-----------------|-----------|
| CustomerID (PK) | int       |
| Mac (PK)        | int       |
| Date            | timestamp |

Table: Customer (DIM)
| Column Name     | Type      |
|-----------------|-----------|
| customerid (PK) | int       |
| mac (PK)        | int       |
| created_date    | timestamp |

Table: CustomerService (DIM)
| Column Name     | Type      |
|-----------------|-----------|
| CustomerID (PK) | int       |
| ServiceID       | int       |
| Amount          | float     |
| Date            | timestamp |

# Goal
The main goal is to provide a comprehensive BI Dashboard or regular reports to track DRM key usage accurately.

# Procedure
1. Load the data from the `MySQL` database
2. Query the data to get the daily usage of DRM keys
3. Create a BI Dashboard or regular reports to track DRM key usage accurately
- keywords: MySQL, BI Dashboard, DBeaver

