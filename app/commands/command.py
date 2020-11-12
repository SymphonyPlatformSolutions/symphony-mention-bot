from sym_api_client_python.clients.sym_bot_client import APIClient
from sym_api_client_python.clients.user_client import UserClient
import codecs, json, os
import asyncio
import logging

## Loading config json files
_configPath = os.path.abspath('./resources/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
        _config = json.load(json_file)

## Use config file
audit_stream = _config['bot_audit']

class Help:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def help(self, msg):

        await asyncio.sleep(0)

        displayHelp = "<card accent='tempo-bg-color--blue' iconSrc=''> \
                            <header><h2>Bot Commands (v1.1)</h2></header> \
                            <body> \
                              <table style='max-width:100%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\"> \
                                    <td><b>Command</b></td> \
                                    <td><b>Description</b></td> \
                                  </tr> \
                                </thead> \
                                <tbody> \
                                  <tr> \
                                    <td>" + _config['bot@Mention'] + " /all</td> \
                                    <td>At Mention all users of the stream</td> \
                                  </tr> \
                                <tr> \
                                  <td>" + _config['bot@Mention'] + " /whois</td> \
                                  <td>followed by @mention will give the user(s) details</td> \
                                </tr> \
                                </tbody> \
                                </table> \
                            </body> \
                        </card>"

        self.help = dict(message="""<messageML>""" + displayHelp + """</messageML>""")
        return self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.help)

## @mention all users of a chat stream (exclude caller user and bot called
class AtRoom():

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def atRoom(self, msg):

        splitter = False
        thereIsMore = False
        once = True
        atMentionLimit = 39
        streamid = msg['stream']['streamId']
        from_user = msg['user']['userId']
        originator = "<mention uid=\"" + str(from_user) + "\"/>"
        botuserid = (self.bot_client.get_bot_user_info())['id']
        mentions = ""
        stream_type = (self.bot_client.get_stream_client().stream_info_v2(streamid))['streamType']['type']

        if str(stream_type) == "IM":
            return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>There is only you and me, """ + str(originator) + """ <emoji shortcode="smile" /></messageML>"""))

        response = self.stream_client.get_room_members(streamid)

        counter = 0
        counterAtmentionedOnly = 0
        totalUsersInRoom = len(response)

        if int(totalUsersInRoom) > int(atMentionLimit):
            splitter = True

        for index in range(len(response)):

            userId = str(response[index]["id"])

            # ## Check the member is not bot
            # userInfo = (UserClient.get_user_from_id(self, userId))['accountType']
            # print(userInfo)

            if (str(userId) == str(from_user)) or (str(userId) == str(botuserid)):# or (str(userInfo) == "SYSTEM"):
                logging.debug("ignored ids")
            else:
                counter += 1
                counterAtmentionedOnly += 1
                mentions += "<mention uid=\"" + userId + "\"/> "

                if splitter and int(counter) == int(atMentionLimit):
                    logging.debug("Displaying @mention")
                    if once:
                        mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header> Room @mentioned by " + str(originator) + "</header><body>" + mentions + "</body></card>"
                        self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))
                        once = False
                    else:
                        mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header></header><body>" + mentions + "</body></card>"
                        self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))

                    counter = 0
                    mentions = ""
                    thereIsMore = True
                    once = False
                elif thereIsMore and (int(totalUsersInRoom) == int(counterAtmentionedOnly) + 2):
                    logging.debug("Displaying @mention for more users")
                    mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header></header><body>" + mentions + "</body></card>"
                    self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))

        if splitter == False:
            logging.debug("Displaying @mention")
            mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header> Room @mentioned by " + str(originator) + "</header><body>" + mentions + "</body></card>"
            self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))


## Get user profile avatar, if none, assign the default Symphony one
class GetAvatar(APIClient):

    def __init__(self, bot_client):
        self.bot_client = bot_client

    ## Get user profile avatar, if none, assign the default Symphony one
    async def getAvatar(self, userid):

        avatar = ""

        try:

            ## This endpoint does not require user provisioning role
            urlcall = "/pod/v3/users?uid=" + str(userid).strip()

            response = self.bot_client.execute_rest_call('GET', urlcall)
            logging.debug(str(response))
            pic = str((response['users'][0]['avatars'][1]['url']))#.replace("/150/","/50/")
            logging.debug(str(pic))

            ## changing default 50 to 150
            if str(pic).startswith("../avatars/static/50/default.png"):
                logging.debug("default avatar 50")
                avatar = _config['podURL'] + "/avatars/static/150/default.png"
                return avatar

            ## Handling when avatar is not uploaded to the right bucket
            if str(pic).startswith("http"):
                logging.debug("None standard URL for Avatar - using s3 bucket, user needs to re-upload avatar")
                avatar = _config['podURL'] + "/avatars/static/150/default.png"
                return avatar

            ## When avatar is correct
            else:
                avatar = str(_config['podURL']) + str(pic).replace("'}", "")
                logging.debug(str(avatar))
                return avatar

        except:
            logging.warning("inside except for avatar")
            avatar = _config['podURL'] + "/avatars/static/150/default.png"
            return (avatar)

class Whois():

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def whois(self, msg_mentions, msg):

        streamid = msg['stream']['streamId']
        externalUser = ""
        external_flag = False
        userid_list = ""
        validUser = False
        userlist = ""
        caller = msg['user']['displayName']

        if len(msg_mentions) <=1:
            logging.warning("Please use the command followed by an @mention")
            return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>Please use the command followed by an @mention</messageML>"""))

        else:

            table_header = ""
            table_body_main = ""

            table_header_main = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:20%'>ID</td>" \
                           "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                           "<td style='max-width:20%'>FIRST NAME</td>" \
                           "<td style='max-width:20%'>LAST NAME</td>" \
                           "<td style='max-width:20%'>DISPLAY NAME</td>" \
                           "</tr></thead><tbody>"

            for x in range(len(msg_mentions)):
                if x >= 1:
                    userInfo = (UserClient.get_user_from_id(self, msg_mentions[x]))

                    try:
                        userid = str(userInfo['id'])
                        logging.debug("User ID: " + str(userid))
                        validUser = True

                    except:
                        userid = str(msg_mentions[x])
                        mention_raw = self.sym_message_parser.get_mentions(msg)
                        mention = str(mention_raw).replace("['", "").replace("', '", ", ").replace("']", "")
                        mention_split_raw = str(mention).split(",")
                        ext_user_raw = str(mention_split_raw[x])
                        ext_user = str(ext_user_raw).replace("@", "")

                        ## Check for dups in external user
                        ## If Dup
                        if str(ext_user) in str(externalUser):
                            continue
                        else:
                            ## No Dup
                            externalUser += str(ext_user) + ", "

                        ## check that only 1 @mention was used (apart from bot itself)
                        if int(len(msg_mentions)) == 2:
                            logging.debug("User is not inside pod: " + (str(externalUser)))
                            usernotinside = "This user," + externalUser + " is not inside your Pod"
                            self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + usernotinside + """</messageML>"""))
                            #Audit
                            if audit_stream != "":
                                self.botaudit = dict(message="""<messageML>/whois This user,""" + externalUser + """ is not inside your Pod)</messageML>""")
                                self.bot_client.get_message_client().send_msg(audit_stream, self.botaudit)
                        else:
                            external_flag = True
                            continue

                    ## Check for dups in userids for display
                    if str(userid) in str(userid_list):
                        continue
                    else:
                        userid_list += str(userid) + ", "

                    try:
                        email = userInfo['emailAddress']
                    except:
                        email = "N/A"
                    try:
                        firstname = userInfo['firstName']
                    except:
                        firstname = "N/A"
                    try:
                        lastname = userInfo['lastName']
                    except:
                        lastname = "N/A"
                    try:
                        displayname = userInfo['displayName']
                    except:
                        displayname = "N/A"
                    try:
                        title = userInfo['title']
                        if str(title) == "":
                            title = "N/A"
                    except:
                        title = "N/A"
                    try:
                        company = userInfo['company']
                    except:
                        company = "N/A"
                    try:
                        username = userInfo['username']
                    except:
                        username = "N/A"
                    try:
                        location = userInfo['location']
                        if str(location) == "":
                            location = "N/A"
                    except:
                        location = "N/A"
                    try:
                        accountype = userInfo['accountType']
                    except:
                        accountype = "N/A"

                    userAvatar_raw = await GetAvatar.getAvatar(self, userid)
                    userAvatar = str(userAvatar_raw).replace("..", "")
                    avatarLink = "<img src=\"" + str(userAvatar) + "\" />"

                    userlist += " - " + str(displayname)

                    table_body_main += "<tr>" \
                      "<td>" + str(userid) + "</td>" \
                      "<td>" + str(email) + "</td>" \
                      "<td>" + str(firstname) + "</td>" \
                      "<td>" + str(lastname) + "</td>" \
                      "<td>" + str(displayname) + "</td>" \
                      "</tr>"

                    ## Card inside Card
                    table_header += "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--black tempo-bg-color--black\">" \
                    "<td style='border:1px solid black;text-align:left' colspan=\"3\"></td></tr><tr>" \
                    "<td style='border:1px solid black;text-align:center;width:7.5%' rowspan=\"10\">" + str(avatarLink) + "</td>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:7.5%;text-align:center'>ID</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(userid) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:7.5%;text-align:center'>EMAIL</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(email) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>FIRSTNAME</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(firstname) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>LASTNAME</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(lastname) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:7.5%;text-align:center'>DISPLAY NAME</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(displayname) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:7.5%;text-align:center'>TIITLE</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(title) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>COMPANY</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(company) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>USERNAME</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(username) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>LOCATION</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(location) + "</td></tr><tr>" \
                    "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>TYPE</td>" \
                    "<td style='border:1px solid black;text-align:center'>" + str(accountype) + " " + "</td></tr></thead><tbody></tbody></table>"

            table_body_main += "</tbody></table>"

            reply_main = table_header_main + table_body_main
            logging.debug(str(reply_main))
            reply = table_header
            logging.debug(str(reply))


            if external_flag and validUser:
                logging.debug("External user: " + str(externalUser[:-2]))
                externalUserMessage = "I am sorry, I am not allowed to look up external users: " + str(externalUser[:-2]) + ""
                self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + externalUserMessage + """</messageML>"""))
                #Audit
                if audit_stream != "":
                    self.botaudit = dict(message="""<messageML>/whois called by """ + str(caller) + """ - External User: """ + str(externalUser[:-2]) + """</messageML>""")
                    self.bot_client.get_message_client().send_msg(audit_stream, self.botaudit)

            elif external_flag:
                logging.debug("External user: " + str(externalUser[:-2]))
                externalUserMessage = "I am sorry, I am not allowed to look up external users: " + str(externalUser[:-2]) + ""
                # Audit
                if audit_stream != "":
                    self.botaudit = dict(message="""<messageML>/whois called by """ + str(caller) + """ - External User: """ + str(externalUser[:-2]) + """</messageML>""")
                    self.bot_client.get_message_client().send_msg(audit_stream, self.botaudit)

                return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + externalUserMessage + """</messageML>"""))

            logging.info("User lookup rendering")
            #Audit
            if audit_stream != "":
                self.botaudit = dict(message="""<messageML>/whois called by """ + str(caller) + """ - Internal User """ + str(userlist) + """</messageML>""")
                self.bot_client.get_message_client().send_msg(audit_stream, self.botaudit)

            whois_card = "<br/><h2>User Details</h2><card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>" + str(reply_main) + "</header><body>" + reply + "</body></card>"
            return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + whois_card + """</messageML>"""))


class SendIMmsg():

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def sendIMmsg(self, StreamClient, userID, firstname, msg):

        ## Gets stream IM of caller and bot
        streamIM = (StreamClient.create_im(self, [str(userID)])['id'])
        ## Sends message to the calling user via IM
        self.imMesage = dict(message="""<messageML>Hi """ + firstname + """, """ + msg + """</messageML>""")
        self.bot_client.get_message_client().send_msg(streamIM, self.imMesage)
