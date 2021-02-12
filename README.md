# Mention
Symphony Room @mention bot by Alex Nalin (Symphony Solutions Architect)

This bot was build using the Symphony Python SDK. (QAed: 1.3.1)

https://developers.symphony.com/symphony-developer/docs/get-started-with-python.


<b>WORKFLOW</b>

Add bot to room and use @mention /all to @mention all members of the stream (Room/MIM/IM)

##

- Commands list:

    @Mention Bot /help
    
    @Mention Bot /all
    
    @Mention Bot /whois


##

- <b>Bot Deployment</b>:

Create a Service Account on your pod:
https://developers.symphony.com/symphony-developer/docs/create-a-bot-user

Generate an RSA Key Pair:

    openssl genrsa -out mykey.pem 4096
    openssl rsa -in mykey.pem -pubout -out pubkey.pem

Copy (zip) or clone this MirrorBot's latest code from private repo (access required):
https://github.com/Alex-Nalin/Mention

Install the required libraries:

    pip install -r requirements.txt

Modify resources\config.json to point to your desired Pod and update the below info about your bot:

    "botPrivateKeyName": "mention_private.pem",
    "botUsername": "MentionBot",
    "bot@Mention": "@MentionBot",
    "botEmailAddress": "mentionbot@symphony.com",
    
Modify the config.json to add your Company name (as visible to others) under allowedPod:

    "allowedPod" : "Symphony Private Pod Name",

You can change log level via config.json, changing to INFO, WARN or DEBUG

    "LOG_LEVEL" : "INFO"
    
You can decide to log to STDERR (useful for docker) or to a log file by updating app/loader/logger.py

STDERR:

    logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w', level=my_level
    )
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)
    
    logger.addHandler(stderr_handler)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

Log File:

    now = datetime.now()
    dt = now.strftime("%d-%m-%Y-%H-%M-%S")
    
    log_dir = os.path.join(os.path.dirname(__file__), "../logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
            filename=os.path.join(log_dir, 'MirrorBot-' + dt +'.log'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='w', level=my_level
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
You can enable bot audit by entering a streamid to receive notification:
(The audit has been enhanced with exception reporting)


    "bot_audit": ""

Starting with Python SDK 1.3, datafeed.id is used to mnanaged session better in case of failure and
you can choose where to store the datafeed.id

    "datafeedIdFilePath": "app"

Start the bot using main_async.py and use "@MentionBot /help" to display the commands

