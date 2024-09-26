from app.models.banco.variaveis import Variaveis
from app import db
import requests, json

class Rq1():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, url, method, set_vars, authorization = None, body :dict = {}) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.url = url
        self.method = method
        self.authorization = authorization
        self.body = body.get('value', None)
        self.body_type = body.get('type', None)
        self.set_vars(set_vars)
    
    def set_vars(self, set_vars):
        if set_vars == None:
            return None
        vars = json.loads(set_vars)
        for var in vars:
            pass

        

    def request(self):
        json = {}
        headers = {}
        if self.authorization:
            headers['Authorization'] = self.authorization
        if self.body_type:
            json = self.body
        response = requests.request(method=self.method, url=self.url, headers=headers, json=json)
        return response.json()
    
    def execute(self, chat_id, dialog_id, **kw):
        pass