# Discord Bot Docker Image

link: ```https://hub.docker.com/repository/docker/shredmetal/olympus-discord-bot/general```

bot invite link: ```https://discord.com/oauth2/authorize?client_id=1253744192363040829&permissions=309237771264&integration_type=0&scope=bot```

Copy and paste the bot invite link into your browser, and invite it to the server.

To run this Discord bot:

1. Ensure Docker is installed on your system.
2. Pull the image:

```docker pull shredmetal/olympus-discord-bot:latest```

3. Run the container:

```docker run -d --name olympus-discord-bot --restart unless-stopped shredmetal/olympus-discord-bot:latest```

4. To stop the bot:

```docker stop olympus-discord-bot```

5. To start the bot again:

```docker start olympus-discord-bot```