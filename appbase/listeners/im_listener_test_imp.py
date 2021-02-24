from sym_api_client_python.listeners.im_listener import IMListener
from .processors.im_processor import IMProcessor, AsyncIMProcessor
import logging


class IMListenerTestImp(IMListener):
    """Example implementation of IMListener
        sym_bot_client: contains clients which respond to incoming events
    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.im_processor = IMProcessor(self.bot_client)

    def on_im_message(self, im_message):
        self.im_processor.process(im_message)

    def on_im_created(self, im_created):
        logging.debug('IM created!', im_created)


class AsyncIMListenerImp(IMListener):
    """Example implementation of IMListener with asynchronous functionality
    Call the bot with /wait to see an example of a non-blocking wait
    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.im_processor = AsyncIMProcessor(self.bot_client)

    async def on_im_message(self, msg):
        logging.debug('message received in IM', msg)

        await self.im_processor.process(msg)

    async def on_im_created(self, im_created):
        logging.debug("IM created!", im_created)