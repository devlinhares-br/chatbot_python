from app.models.bitrix.bitrix import Bitrix
from app.models.banco.variaveis import Variaveis
from app import db
import re

class Gt():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, var_name, proximo_bloco, regex=None, mensagem_invalido=None, update=False) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.__var_name = var_name
        self.__var_value = None
        self.proximo_bloco = proximo_bloco
        self.regex = regex
        self.mensagem_invalido = mensagem_invalido
        self.update = update
        self.__bitrix = Bitrix()
    
    def set_var(self, value:str)->None:
        self.__var_value = value
 
    
    def get_value(self):
        return self.__var_value
    
    def __send_menssage_invalid(self, dialog_id:str|int):
        return self.__bitrix.send_menssage(self.mensagem_invalido, dialog_id)
    
    def get_var_name(self):
        return self.__var_name
    
    def __save_var(self, var_name, var_value, dialog_id):
        variavel = Variaveis.query.filter_by(dialog_id=dialog_id, name=var_name).first()
        if variavel:
            variavel.value = f'{variavel.value}\n{var_value}' if self.update else var_value
            Variaveis.query.filter_by(dialog_id=dialog_id, name=var_name).update(variavel.to_dict())
            db.session.commit()
        else:
            nova_variavel = Variaveis(dialog_id, var_name, var_value)
            db.session.add(nova_variavel)
            db.session.commit()
    
    def get_proximo_bloco(self):
        return self.proximo_bloco
    
    def execute(self, chat_id, dialog_id, **kw):
        if self.regex is not None:
            resultado = re.search(self.regex, kw['user_last_message'])
            if resultado:
                self.__save_var(self.get_var_name(), resultado.group(), dialog_id)
            else:
                self.__send_menssage_invalid(dialog_id)
                return self.id_bloco_anterior
        else:
            self.__save_var(self.get_var_name(), kw['user_last_message'], dialog_id)
        return self.get_proximo_bloco()
    