class DataMessage():
    def __init__(self, data:dict) -> None:
        self.event = data.get('event', '')
        self.bot = Bot(data)
        self.params = Params(data)
        self.user = User(data)
        self.auth = Auth(data)
    

class Bot():
    def __init__(self, data:dict) -> None:
        self.bot_id = data.get('data[BOT][1438][BOT_ID]', '')
        self.bot_code = data.get('data[BOT][1438][BOT_CODE]', '')

class Params():
    def __init__(self, data:dict) -> None:
        self.from_user_id = data.get('data[PARAMS][FROM_USER_ID]', '')
        self.message = data.get('data[PARAMS][MESSAGE]', '')
        self.to_chat_id = data.get('data[PARAMS][TO_CHAT_ID]', '')
        self.message_type = data.get('data[PARAMS][MESSAGE_TYPE]', '')
        self.author_id = data.get('[PARAMS][AUTHOR_ID]', '')
        self.chat_id = data.get('data[PARAMS][CHAT_ID]', '')
        self.chat_author_id = data.get('data[PARAMS][CHAT_AUTHOR_ID]', '')
        self.chat_entity_type = data.get('data[PARAMS][CHAT_ENTITY_TYPE]', '')
        self.chat_entity_id = self.set_chat_entity_id(data.get('data[PARAM][CHAT_ENTITY_ID]', ''))
        self.chat_entity_data_1 = self.set_chat_entity_data_1(data.get('data[PARAMS][CHAT_ENTITY_DATA_1]', ''))
        self.to_user_id = data.get('data[PARAMS][TO_USER_ID]', '')
        self.dialog_id = data.get('data[PARAMS][DIALOG_ID]', '')
    
    def set_chat_entity_id(self, value:str) -> list:
        return value.split('|')
    
    def set_chat_entity_data_1(self, value:str) -> list:
        return value.split('|')

class User():
    def __init__(self, data:dict) -> None:
        self.id = data.get('data[USER][ID]', '')
        self.name = data.get('data[USER][NAME]', '')
        self.first_name = data.get('data[USER][FIRST_NAME]', '')
        self.last_name = data.get('data[USER][LAST_NAME]', '')
        self.is_extranet = data.get('data[USER][IS_EXTRANET]', '')

class Auth():
    def __init__(self, data:dict) -> None:
        self.domain = data.get('auth[domain]', '')
        self.aplication_token = data.get('auth[application_token]','')