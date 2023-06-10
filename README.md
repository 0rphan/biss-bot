# Discord bot for BISS use

This discord bot is used to make discord server of biss much better.
The bot include several commands that well be broken down later.
Use the bot carefully when deploying.

Written by TC.

---

# File Hierarchy

* cogs - Folder used to hold bot command groups.
    * biss.py - biss commands, maily edit this.
    * fun.py - random commands.
    * general.py - general bot commands.
    * moderation.py - classic moderator commands.
    * owner.py - special commands for bot deployer.
* database - holds all the database related file
* exceptions - holds custom exception classes
* helpers - hold all needed helper functions
* bot.py - main file, the bot itself
* config.json - our config file
---
### config.json
```json
{
  "prefix": "<PREFIX>",
  "token": "<BOT_TOKEN>",
  "permissions": "8",
  "application_id": "1111198676442955838",
  "sync_commands_globally": false,
  "owners": [
    263731878622789633
  ]
}

```

`prefix` can be changed to your liking, default `?` \
`token` is the bot token from the [discord developer portal](https://discord.com/developers/applications)

---
# Requirements

The list of requirements is short and easy, use the lateset of all
* aiohttp
* aiosqlite
* discord.py