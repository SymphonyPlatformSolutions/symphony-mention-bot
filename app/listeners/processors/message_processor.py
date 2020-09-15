from sym_api_client_python.clients.user_client import UserClient
from app.commands.command import AtRoom, Help, Whois
import defusedxml.ElementTree as ET
import logging
import codecs
import json
import os


## json config file def
_configPath = os.path.abspath('./resources/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
        _config = json.load(json_file)


'''
Performance improvement:
Takes the date and time stored initially when the bot is executed, compares it with the time now when the function is called, if more than set time (5 mins default)
reload the list, create the new form entry, otherwise use existing client list
'''


"""This will process the message posted in Symphony UI"""
class MessageProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def processor(self, msg):

        podAllowed = False
        mention = ""
        mention_len = ""

        try:
            firstname = msg['user']['firstName']
        except:
            firstname = "N/A"
        try:
            lastname = msg['user']['lastName']
        except:
            lastname = "N/A"
        displayName = msg['user']['displayName']
        email = msg['user']['email']
        userID = msg['user']['userId']
        try:
            username = msg['user']['username']
        except:
            username = "N/A"
        streamID = msg['stream']['streamId']
        streamType = msg['stream']['streamType']


        userFromid = UserClient.get_user_from_id(self, userID)
        userCompany = (userFromid['company'])

        logging.debug("--> User ID: " + str(userID) + " & full name: " + str(firstname) + " " + str(lastname))
        try:
            logging.debug("--> User email: " + str(email) + " & username: " + str(username) + " display Name: " + str(displayName))
        except:
            logging.debug("--> User email: " + str(email) + " & displayName: " + str(displayName))

        logging.debug("--> Stream Type: " + str(streamType) + " with stream ID: " + str(streamID))
        logging.debug("--> User is from: \"" + userCompany + "\" pod")

        ## Normal message in the chat - no @mention of #hashtag nor $cashtag
        msg_xml = msg['message']
        msg_root = ET.fromstring(msg_xml)
        msg_text = msg_root[0].text
        logging.debug(msg_text)

        try:
            ## Get the command send and check its lenght
            message_raw = self.sym_message_parser.get_text(msg)
            list_len = int(len(message_raw))

            ## Adds the items to one variable
            var_raw = ""
            for l in range(list_len):
                var_raw += str(message_raw[l]) + " "

            message_reader = str(var_raw).replace("[", "").replace("'", "").replace("]", "")
            logging.debug("message_reader: " + str(message_reader))

        except:
            return await Help.help(self, msg)

        ## Getting @mention details
        try:
            mention_raw = self.sym_message_parser.get_mentions(msg)
            mention = str(mention_raw).replace("['", "").replace("', '", ", ").replace("']", "")
            logging.debug("mentions, hashtags, cashtags: " + str(mention))
            mention_split = str(mention).split(",")
            mention_len = len(str(mention_split[0]))
            firstMention = mention_split[0]
            logging.debug("firstMention: " + str(firstMention))
        except:
            firstMention = mention
            logging.debug("No @mention",  exc_info=True)

        """
        This is to make sure the user is from the allowed pod(s)
        """
        if userCompany in _config['allowedPod']:
            logging.debug("Inside allowed Pod(s), True")
            podAllowed = True
        else:
            podAllowed = False
            logging.debug("Outside allowed Pod(s), False")


        try:
            ## If within allowed Pod
            if podAllowed:

                ## Making sure the bot @mention is used and matches to respond back
                if str(firstMention) == str(_config['bot@Mention']):
                    logging.debug("mention: " + str(mention))
                    commandName = str(message_reader)[int(mention_len)+1:]
                    logging.debug("commandName: " + str(commandName))

                    try:
                        if "/all" in str(commandName):
                            logging.info("Calling /all by " + str(displayName))
                            return await AtRoom.atRoom(self, msg)
                    except:
                        logging.error("/all is not working")
                        return logging.debug("/all is not working", exc_info=True)

                    try:
                        if "/whois" in str(commandName):
                            logging.info("Calling /whois by " + str(displayName))
                            msg_mentions = self.sym_message_parser.get_mention_ids(msg)
                            return await Whois.whois(self, msg_mentions, msg)
                    except:
                        logging.error("/whois is not working")
                        return logging.debug("/whois is not working", exc_info=True)

                    try:
                        ## Help command when called via :@mention /help call
                        if "/help" in str(commandName):
                            logging.info("Calling /help by " + str(displayName))
                            return await Help.help(self, msg)
                    except:
                        logging.error("/help is not working")
                        return logging.debug("Help is not working",  exc_info=True)

                else:
                    return logging.debug("bot @mentioned does not match expected, or not calling bot command")
            else:
                return logging.debug("User is not from the allowed Pod(s)")
        except:
            return logging.debug("bot @mentioned was not used",  exc_info=True)