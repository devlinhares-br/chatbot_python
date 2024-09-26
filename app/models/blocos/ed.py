from app.models.bitrix.bitrix import Bitrix
from app.models.banco.conversas import Conversas
from app.models.banco.variaveis import Variaveis
from app import db

class Ed():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, encerra_conversa_bitrix) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.encerra_conversa_bitrix = encerra_conversa_bitrix
        self.__bitrix = Bitrix()
    
    def __dict__(self):
        return {
            'id_bloco': self.id_bloco,
            'identificador': self.identificador,
            'id_bloco_anterior': self.id_bloco_anterior,
            'encerra_conversa_bitrix': self.encerra_conversa_bitrix
        }

    def finaliza_conversa_db(self, dialog_id):
        self.__delete_conversa(dialog_id)
        print(self.__deletar_variaveis(dialog_id))
        return True

    def __deletar_variaveis(self, dialog_id):
        variaveis = Variaveis.query.filter_by(dialog_id=dialog_id).all()
        if variaveis:
            for variavel in variaveis:
                db.session.delete(variavel)
                db.session.commit()
            return True
        return False

    def __delete_conversa(self, dialog_id):
        conversas = Conversas.query.filter_by(dialog_id=dialog_id)
        print(conversas)
        if conversas:
            for conversa in conversas:
                db.session.delete(conversa)
                db.session.commit()
            return True
        return False

    def to_dict(self):
        return {
            'id_bloco': self.id_bloco
        }

    def execute(self, chat_id, dialog_id, **kw):
        if self.encerra_conversa_bitrix:
            self.__bitrix.end_conversation(chat_id)
        self.__bitrix.quit_chat(chat_id)
        self.finaliza_conversa_db(dialog_id)
        return -1
    