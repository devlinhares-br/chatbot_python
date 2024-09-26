from app.models.banco.variaveis import Variaveis
from app.models.bitrix.DataUser import DataUser
from app.services.tratamentos.tratamentos import *
import requests, re

class Bitrix():
    __BASE_URL = 'https://b24-xyu0fb.bitrix24.com.br/rest/9/ne0pa14bhqavrnd5/'
    __CODE_ID = 'a7rh5qv5u7471y21'
    __CLIENT_ID = '8iqtzzk9q9aghsiy6sqn54j6fkyw1s38'
    __BOT_ID = '15'

    __METODOS = {
        'message_add': 'imbot.message.add.json/',
        'session_finish': 'imopenlines.bot.session.finish.json/',
        'session_transfer': 'imopenlines.bot.session.transfer.json/',
        'chat_leave': 'imbot.chat.leave',
        'im_user_get': 'im.user.get.json',
        'chat_user_list': 'imbot.chat.user.list',
        'dialog_user_list': 'im.dialog.users.list.json',
        'crm_chat_get': 'imopenlines.crm.chat.get.json',
        'crm_deal_update': 'crm.deal.update.json',
        'crm_deal_get': 'crm.deal.get.json',
        'workflow_ex': 'bizproc.workflow.start'
    }

    def __init__(self) -> None:
        pass

    def get_bot_id(self):
        return self.__BOT_ID
    
    def __requests(self, metodo:str, json:dict):
        # Monta a url para requisição
        url = f'{self.__BASE_URL}{metodo}'
        # adiciona a authenticação na requisição
        auth = {
            'CLIENT_ID': self.__CLIENT_ID,
            'BOT_ID': self.__BOT_ID
        }
        json.update(auth)

        response = requests.post(url, json=json)
        response_json = response.json()
        if 'result' in response_json:
            return True, response_json, response.status_code
        else:
            return False, response_json, response.status_code


    # Send Mensage
    def send_menssage(self, text, dialog_id, system_message:str = 'N'):
        variaveis = get_variaveis(dialog_id)
        text = substituir_variaveis(text, variaveis)
        raw = {
            'DIALOG_ID': dialog_id,
            'MESSAGE': text,
            'SYSTEM': system_message
        }
        return self.__requests(self.__METODOS["message_add"], raw)


    def trasnfer_to_user(self, user_id, chat_id):
        raw = {
            'USER_ID': user_id,
            'CHAT_ID': chat_id,
        }
        return self.__requests(self.__METODOS["session_transfer"], raw)

    def transfer_to_group(self, group_id, chat_id):
        raw = {
            'QUEUE_ID': group_id,
            'CHAT_ID': chat_id,
        }
        return self.__requests(self.__METODOS["session_transfer"], raw)

    def quit_chat(self, chat_id):
        raw = {
            'CHAT_ID': chat_id
        }
        return self.__requests(self.__METODOS["chat_leave"], raw)

    def update_title(self, new_title, collor):
        pass

    def end_conversation(self, chat_id):
        raw = {
            'CHAT_ID': chat_id
        }
        return self.__requests(self.__METODOS["session_finish"], raw)
    
    def im_user_get(self, user_id)->DataUser:
        raw = {
            'ID': user_id
        }
        response = self.__requests(self.__METODOS['im_user_get'], raw)
        print(response)
        response = response[1]
        user = DataUser(response.get('result', {}))
        return user
    
    def list_chat_user(self, chat_id)->dict:
        raw = {
            'CHAT_ID': chat_id
        }
        response = self.__requests(self.__METODOS['chat_user_list'], raw)
        print(response)
        return response[1]['result']
    
    def list_dialog_user(self, dialog_id):
        raw = {
            'DIALOG_ID': dialog_id
        }
        response = self.__requests(self.__METODOS['dialog_user_list'], raw)
        return response[1]

    
    def crm_chat_get(self, entity_type:str, entity_id:int):
        """crm_chat_get

        Args:
            entity_type (str): Tipo de entidade: lead, deal, contact, company
            entity_id (int): id da entidade

        Returns:
            dict: retorno da requisição
        """
        raw = {
            "CRM_ENTITY_TYPE": entity_type,
            "CRM_ENTITY": entity_id
        }
        response = self.__requests(self.__METODOS['crm_chat_get'], raw)
        return response
    
    def move_card(self, id, pipe= 0):
        raw = {
            "DOCUMENT_ID": ["crm", "CCrmDocumentDeal", f"DEAL_{id}"],
            "TEMPLATE_ID": 43,
            "PARAMETERS": {
                "pipe": pipe
            }
        }
        response = self.__requests(self.__METODOS['workflow_ex'], raw)
        return response
    
    def get_card(self, id):
        raw = {
            "ID": id
        }
        response = self.__requests(self.__METODOS['crm_deal_get'], raw)
        return response[1]