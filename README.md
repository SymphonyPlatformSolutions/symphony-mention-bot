# Mention
Symphony Room @mention bot

This bot was build using the Symphony Python SDK.

https://developers.symphony.com/symphony-developer/docs/get-started-with-python.


<b>WORKFLOW</b>

Add bot to room and use @mention /all to @mention all members of the stream (Room/MIM/IM)

##

- Commands list:

    @Mention Bot /help
    
    @Mention Bot /all
    
    @Mention Bot /whois


##

- Bot Deployment:

Create a Service Account on your pod:
https://developers.symphony.com/symphony-developer/docs/create-a-bot-user

Copy this Mention Bot's latest code from private repo (access required):
https://github.com/Alex-Nalin/Mention

Modify resources\config.json to point to your desired Pod and update the below info about your bot:

    "botPrivateKeyName": "mention_private.pem",
    "botUsername": "MentionBot",
    "bot@Mention": "@MentionBot",
    "botEmailAddress": "mentionbot@symphony.com",
    
Modify the config.json to add your Pod name under allowedPod:

    "allowedPod" : "Symphony Partner Development, Symphony Preview Pod",

You can change log level via config.json, changing to INFO, WARN or DEBUG

    "LOG_LEVEL" : "INFO"
    
Start the bot using main_async.py and use "@MentionBot /help" to display the commands

