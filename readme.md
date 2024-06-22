# The Olympus Discord Bot

This bot is intended to be deployed on the DCS Olympus Discord. More features are planned for later releases.

Many thanks to the tireless DCS Olympus team members who trawled the internet hunting down a whole bunch of gifs 
tangentially related to logs.

## Features

- Responds to the `/support` command by checking for required log files and providing feedback.
- Sends random GIFs when logs are not attached.
- Utilizes privileged intents to read message content.

## Prerequisites

- Docker
- Docker Compose
- A Discord bot token with the necessary permissions and intents enabled.

## Setup

### 1. Clone the Repository

```git clone <repository-url> cd <repository-directory>```

### 2. Create a `.env` File

Create a `.env` file in the root directory of your project and add your Discord bot token:

```DISCORD_TOKEN=your_actual_discord_token```


### 3. Build and Run the Docker Container

Use the provided deploy script to build and run the Docker container:

```sh deploy.sh```

### 4. Invite the Bot to Your Discord Server

@WirtsLegs if you are reading this I already gave you the link in the Admin channel.

Generate an invite link for your bot with the necessary permissions:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications/).
2. Select your application.
3. Navigate to the "OAuth2" section.
4. Under the "OAuth2" section, click on the "URL Generator" tab.
5. In the "Scopes" section, select the `bot` scope.
6. In the "Bot Permissions" section, select the following permissions:
   - `Send Messages`
   - `Read Message History`
   - `Attach Files`
   - `Embed Links`
   - `Add Reactions`
   - `Manage Messages`
7. Copy the generated URL and paste it into your web browser.
8. Select the server where you have the `Manage Server` permission and authorize the bot.

## Usage

Once the bot is up and running, you can use the `/support` command in your Discord server to interact with the bot.

### Example Command

```/support```

The bot will check for required log files and provide feedback. If no logs are attached, it will send a random GIF.

## Development

### Running the Bot Locally

1. Ensure you have Python 3.11+ and `pip` installed.
2. Install the required Python packages:

```pip install -r requirements.txt```

3. Run the bot:

```python bot.py```


