from app.models.bitrix.bitrix import Bitrix

class Ms():
    def __init__(self, id_bloco, identificador ,id_bloco_anterior, mensagens:list, proximo_bloco, system_message, aguarde) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.__get_mensagens(mensagens)
        self.proximo_bloco = proximo_bloco
        self.system_message = system_message
        self.aguarde = aguarde
        self.__bitrix = Bitrix()
    
    def __send_menssage(self, dialog_id) -> None:
        for message in self.mensagens:
            self.__bitrix.send_menssage(message, dialog_id, self.system_message)

    def __get_mensagens(self, mensagens=[]):
        self.mensagens = mensagens

    def __get_next_block(self):
        return self.proximo_bloco

    def __get_aguarde(self):
        return self.aguarde
    
    def __get_block_id(self):
        return self.id_bloco
    
    
    def to_dict(self):
        return {
            'id_bloco': self.id_bloco
        }
    
    def execute(self, chat_id, dialog_id, **kw):
        self.__send_menssage(dialog_id)
        if self.__get_aguarde():
            return False
        else:
            return self.__get_next_block()