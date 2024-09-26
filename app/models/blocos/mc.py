from app.models.bitrix.bitrix import Bitrix

class Mc():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, pipe, etapa, proximo_bloco) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.proximo_bloco = proximo_bloco
        self.pipe = pipe
        self.etapa = etapa
        self.__bitrix = Bitrix()

    
    def __move_card(self, id):
        return self.__bitrix.move_card(id, self.pipe)
    
    def get_proximo_bloco(self):
        return self.proximo_bloco

    def execute(self, chat_id, dialog_id, **kw):
        if kw.get('deal', 0):
            self.__move_card(kw.get('deal', 0))
        return self.get_proximo_bloco()