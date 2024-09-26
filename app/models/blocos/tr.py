from app.models.bitrix.bitrix import Bitrix

class Tr():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, is_user, to_id, mensagem, proximo_bloco) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.is_user = is_user
        self.to_id = to_id
        self.mensagem = mensagem
        self.proximo_bloco = proximo_bloco
        self.__bitrix = Bitrix()

    def __send_message(self, dialog_id):
        return self.__bitrix.send_menssage(self.mensagem, dialog_id)
    
    def __transfer(self, chat_id):
        if self.is_user:
            return self.__bitrix.trasnfer_to_user(self.to_id, chat_id)
        return self.__bitrix.transfer_to_group(self.to_id, chat_id)
    
    def get_proximo_bloco(self):
        return self.proximo_bloco

    def execute(self, chat_id, dialog_id, **kw):
        self.__send_message(dialog_id)
        self.__transfer(chat_id)
        return self.get_proximo_bloco()