# Goals
- [x] Make a simple Discord bot that can be used to interact with users

# Procedure
- Step 1: Create a Discord server
- Step 2: Create a Discord bot:
  - Step 2.1: Go to [Discord application page](https://discord.com/developers/applications/) and click `New Applications` button to create a new application, set the name of the application e.g., `super-bot`
  - Step 2.2: Click the new icon of the application to go to the setting page
  - Step 2.3: Click `General Information` tab, set up some general information of the bot
  - Step 2.4: Click `Bot` tab, find the option `Message Content Intent` and activate it
  - Step 2.5: Click `Reset Token` then copy and past the token to the `.env_template.template` file, then rename to `.env` for later use
  - Step 2.6: Click the `OAuth2` tab, find the box `OAuth2 URL Generator` and tick `bot`. The `BOT PERMISSIONS` field will then appear.
  - Step 2.7: At `BOT PERMISSIONS` box, some basic permissions such as: `Send Message`, `Read Message History`, `View Channels`
  - Step 2.8: At the bottom of the curren website page, copy the generated URL and paste it into the browser, select the server you want to add the bot to. The bot will be available in the server but still be offline at this point
- Step 3: Install the Discord library by using `pip install discord.py`
- Step 4: clone the repository [here](https://github.com/haison19952013/Personal-Data-Science-Projects/tree/0372335910fe134f2cab3da70427e7b213ae974b/Discord%20Bot%20Sample) and run `main.py` to start the bot. The bot will be online and ready to interact with users
