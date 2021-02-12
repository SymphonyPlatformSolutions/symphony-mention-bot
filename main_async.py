import argparse
import asyncio
import logging
import app.loader as loader

from sym_api_client_python.auth.auth import Auth
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig
from app.listeners.im_listener_test_imp import AsyncIMListenerImp
from app.listeners.room_listener_test_imp import AsyncRoomListenerImp

loopCount = 0
def main():
        global loopCount

        parser = argparse.ArgumentParser()
        parser.add_argument("--auth", choices=["rsa", "cert"], default="rsa", help="Authentication method to use")
        parser.add_argument("--config", help="Config json file to be used")

        args = parser.parse_args()

        configure = SymConfig(loader.config._configPath)
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
        logging.info('Datafeed started - bot is ready')
        loop = asyncio.get_event_loop()
        awaitables = asyncio.gather(datafeed_event_service.start_datafeed())
        loop.run_until_complete(awaitables)



if __name__ == "__main__":
    main()
    ## Not needed for Docker
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