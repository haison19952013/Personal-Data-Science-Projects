# Motivation
- Due to the lack of API for getting job information, there is a need to develop a tool to retrieve job information from various popular jobs websites such as [itviec.com](https://itviec.com/),[topdev.vn](https://topdev.vn/), etc.

# Goals
- [x] Develop a tool to retrieve job information from a single website [itviec.com](https://itviec.com/)
- [x] The tool then is integrated into a Discord bot to provide job information to users based on their personal preferences
- [ ] Generalize the tools for more websites such as [topdev.vn](https://topdev.vn/), [linkedin.com](https://linkedin.com), etc.
- [ ] Use the database such as MySQL to store job information rather than just .csv files


# Data Dictionary
| Columne Name   | Type     |
|----------------|----------|
| job link       | str      |
| job title      | str      |
| company name   | str      |
| location       | str      |
| work type      | str      |
| jd             | str      |
| requirement    | str      |
| posted time    | datetime |
| thumbnail link | str      |

# Procedure
- Construct `job_tools.py`, including functions to scrape job information from [itviec.com](https://itviec.com/)
- Construct `discord_bot.py` to interact with users commands and processes them. This script will require a Discord bot token to run. 
- Construct `responses.py` to receive responses from users and return job information based on their preferences using functions from `job_tools.py`
- Create a Discord server, create an Discord application, create a bot, generate the token, and invite the bot to the server (see the [tutorial](https://www.youtube.com/watch?v=itLd9-U6UBA))

