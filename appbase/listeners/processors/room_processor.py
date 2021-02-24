from sym_api_client_python.processors.sym_message_parser import SymMessageParser
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.clients.stream_client import StreamClient
from appbase.listeners.processors.message_processor import MessageProcessor as message_processor
import logging

class RoomProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.message_formatter = MessageFormatter()
        self.sym_message_parser = SymMessageParser()
        self.stream_client = StreamClient(bot_client)

    #reads message and processes it
    def process(self, msg):
        logging.debug('room_processor/process_room_message()')
        message_processor.processor(self, msg)

class AsyncRoomProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.message_formatter = MessageFormatter()
        self.sym_message_parser = SymMessageParser()
        self.stream_client = StreamClient(bot_client)

    async def process(self, msg):
        logging.debug('room_processor/process_room_message()')
        await message_processor.processor(self, msg)