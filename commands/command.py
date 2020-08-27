from sym_api_client_python.clients.user_client import UserClient
import codecs, json, os
import asyncio
import logging

## Loading config json files
_configPath = os.path.abspath('./resources/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
        _config = json.load(json_file)

class Help:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def help(self, msg):

        await asyncio.sleep(0)

        displayHelp = "<card accent='tempo-bg-color--blue' iconSrc=''> \
                            <header><h2>Bot Commands (v1.2) </h2></header> \
                            <body> \
                              <table style='max-width:100%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\"> \
                                    <td><b>Command</b></td> \
                                    <td><b>Description</b></td> \
                                    <td><b>Permission</b></td> \
                                  </tr> \
                                </thead> \
                                <tbody> \
                                  <tr> \
                                    <td>" + _config['bot@Mention'] + " /all</td> \
                                    <td>At Mention all users of the stream</td> \
                                    <td>All</td> \
                                  </tr> \
                                <tr> \
                                  <td>" + _config['bot@Mention'] + " /whois</td> \
                                  <td>followed by @atmention will give the user(s) details</td> \
                                  <td>All</td> \
                                </tr> \
                                </tbody> \
                                </table> \
                            </body> \
                        </card>"

        self.help = dict(message="""<messageML>""" + displayHelp + """</messageML>""")
        return self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.help)

    async def helpAdmin(self, msg):

        await asyncio.sleep(0)

        displayHelp = "<card accent='tempo-bg-color--blue' iconSrc=''> \
                            <header><h2>Bot Commands (v1 (Admin)</h2></header> \
                            <body> \
                              <table style='max-width:100%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\"> \
                                    <td><b>Command</b></td> \
                                    <td><b>Description</b></td> \
                                    <td><b>Permission</b></td> \
                                  </tr> \
                                </thead> \
                                <tbody> \
                                <tr> \
                                    <td>" + _config['bot@Mention'] + " /all</td> \
                                    <td>At Mention all users of the stream</td> \
                                  <td>Bot Admin</td> \
                                </tr> \
                                <tr> \
                                  <td>" + _config['bot@Mention'] + " /whois</td> \
                                  <td>followed by @atmention will give the user(s) details</td> \
                                  <td>All</td> \
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

        response = self.stream_client.get_room_members(streamid)

        counter = 0
        counterAtmentionedOnly = 0
        totalUsersInRoom = len(response)

        if int(totalUsersInRoom) > int(atMentionLimit):
            splitter = True

        for index in range(len(response)):

            userId = str(response[index]["id"])
            if (str(userId) == str(from_user)) or (str(userId) == str(botuserid)):
                logging.debug("ignored ids")
            else:
                counter += 1
                counterAtmentionedOnly += 1
                mentions += "<mention uid=\"" + userId + "\"/> "

                if splitter and int(counter) == int(atMentionLimit):
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
                    mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header></header><body>" + mentions + "</body></card>"
                    self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))

        if splitter == False:
            mention_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header> Room @mentioned by " + str(originator) + "</header><body>" + mentions + "</body></card>"
            self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + mention_card + """</messageML>"""))


class Whois():

    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def whois(self, msg_mentions, msg):

        streamid = msg['stream']['streamId']

        if len(msg_mentions) <=1:
            return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>Please use the command followed by an @mention</messageML>"""))

        else:

            table_body = ""
            table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:20%'>ID</td>" \
                           "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                           "<td style='max-width:20%'>FIRST NAME</td>" \
                           "<td style='max-width:20%'>LAST NAME</td>" \
                           "<td style='max-width:20%'>DISPLAY NAME</td>" \
                           "<td style='max-width:20%'>TITLE</td>" \
                           "<td style='max-width:20%'>COMPANY</td>" \
                           "<td style='max-width:20%'>USERNAME</td>" \
                           "<td style='max-width:20%'>LOCATION</td>" \
                           "<td style='max-width:20%'>ACCOUNT TYPE</td>" \
                           "</tr></thead><tbody>"

            for x in range(len(msg_mentions)):
                if x >= 1:
                    userInfo = (UserClient.get_user_from_id(self, msg_mentions[x]))
                    userid = userInfo['id']
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
                    except:
                        title = "N/A"
                    company = userInfo['company']
                    try:
                        username = userInfo['username']
                    except:
                        username = "N/A"
                    try:
                        location = userInfo['location']
                    except:
                        location = "N/A"
                    try:
                        accountype = userInfo['accountType']
                    except:
                        accountype = "N/A"

                    table_body += "<tr>" \
                      "<td>" + str(userid) + "</td>" \
                      "<td>" + str(email) + "</td>" \
                      "<td>" + str(firstname) + "</td>" \
                      "<td>" + str(lastname) + "</td>" \
                      "<td>" + str(displayname) + "</td>" \
                      "<td>" + str(title) + "</td>" \
                      "<td>" + str(company) + "</td>" \
                      "<td>" + str(username) + "</td>" \
                      "<td>" + str(location) + "</td>" \
                      "<td>" + str(accountype) + "</td>" \
                      "</tr>"

            table_body += "</tbody></table>"

            reply = table_header + table_body

            whois_card = "<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>"
            return self.bot_client.get_message_client().send_msg(streamid, dict(message="""<messageML>""" + whois_card + """</messageML>"""))

