from app.listeners.processors.message_processor import MessageProcessor as message_processor
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.clients.stream_client import StreamClient
import logging

class IMProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.message_formatter = MessageFormatter()
        self.sym_message_parser = SymMessageParser()
        self.stream_client = StreamClient(bot_client)

    def process(self, msg):
        logging.debug('im_processor/process_im_message()')
        message_processor.processor(self, msg)

class AsyncIMProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.message_formatter = MessageFormatter()
        self.sym_message_parser = SymMessageParser()
        self.stream_client = StreamClient(bot_client)

    async def process(self, msg):
        logging.debug('im_processor/process_im_message()')
        await message_processor.processor(self, msg)
