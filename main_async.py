import argparse
import asyncio
import logging
import time
import os, sys

from sym_api_client_python.auth.auth import Auth
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig
from listeners.im_listener_test_imp import AsyncIMListenerImp
from listeners.room_listener_test_imp import AsyncRoomListenerImp
# from sym_api_client_python.listeners.im_listener_test_imp import AsyncIMListenerImp
# from sym_api_client_python.listeners.room_listener_test_imp import AsyncRoomListenerImp


def configure_logging():
        logging.basicConfig(
                stream=sys.stdout,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='w', level=logging.DEBUG
        )
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(formatter)

        logger.addHandler(stderr_handler)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

### logs to file
# def configure_logging():
#         log_dir = os.path.join(os.path.dirname(__file__), "logs")
#         if not os.path.exists(log_dir):
#             os.makedirs(log_dir, exist_ok=True)
#         logging.basicConfig(
#                 filename=os.path.join(log_dir, 'MentionBot.log'),
#                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                 filemode='w', level=logging.DEBUG
#         )
#         logging.getLogger("urllib3").setLevel(logging.WARNING)

# def configure_logging():
#
#         logging.basicConfig(
#                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                 level=logging.DEBUG
#         )
#         logging.getLogger("urllib3").setLevel(logging.WARNING)


loopCount = 0
def main():
        global loopCount

        parser = argparse.ArgumentParser()
        parser.add_argument("--auth", choices=["rsa", "cert"], default="rsa", help="Authentication method to use")
        parser.add_argument("--config", help="Config json file to be used")

        args = parser.parse_args()

        # Configure log
        configure_logging()

        # Cert Auth flow: pass path to certificate config.json file
        if args.config is None:
            config_path = os.path.join(os.path.dirname(__file__), "resources", "config.json")
        else:
            config_path = args.config

        configure = SymConfig(config_path, config_path)
        configure.load_config()

        if args.auth == "rsa":
            auth = SymBotRSAAuth(configure)
        elif args.auth == "cert":
            auth = Auth(configure)
        else:
            raise ValueError("Unexpected value for auth: " + args.auth)

        auth.authenticate()

        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)

        # Initialize datafeed service
        datafeed_event_service = bot_client.get_async_datafeed_event_service()

        # Initialize listener objects and append them to datafeed_event_service
        # Datafeed_event_service polls the datafeed and the event listeners
        # respond to the respective types of events
        im_listener_test = AsyncIMListenerImp(bot_client)
        datafeed_event_service.add_im_listener(im_listener_test)
        room_listener_test = AsyncRoomListenerImp(bot_client)
        datafeed_event_service.add_room_listener(room_listener_test)

        # Create and read the datafeed
        logging.debug('Starting datafeed')
        loop = asyncio.get_event_loop()
        awaitables = asyncio.gather(datafeed_event_service.start_datafeed())
        loop.run_until_complete(awaitables)


if __name__ == "__main__":
    main()
    # while loopCount < 10:
    #     try:
    #         main()
    #     except SystemExit:
    #         loopCount = 99
    #         pass
    #     except Exception as ex:
    #         logging.debug('Error: ' + str(ex))
    #         logging.debug('Unhandled error, probably network difficulties at the Agent. Retrying in 10s.')
    #         print('Unhandled error, probably network difficulties at the Agent. Retrying in 10s.')
    #         time.sleep(1)
    #         loopCount += 1