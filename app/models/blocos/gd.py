from app.models.bitrix.bitrix import Bitrix
from app.models.banco.variaveis import Variaveis
from app import db

class Gd():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, var_name, field, proximo_bloco) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.proximo_bloco = proximo_bloco
        self.var_name = var_name
        self.field = field
        self.__bitrix = Bitrix()

    
    def __get_card(self, id, campo):
        card = self.__bitrix.get_card(id)
        card = card.get('result')
        return card.get(campo, '')
    
    def get_proximo_bloco(self):
        return self.proximo_bloco
    
    def __save_var(self, var_name, var_value, dialog_id):
        variavel = Variaveis.query.filter_by(dialog_id=dialog_id, name=var_name).first()
        if variavel:
            variavel.value = var_value
            Variaveis.query.filter_by(dialog_id=dialog_id, name=var_name).update(variavel.to_dict())
            db.session.commit()
        else:
            nova_variavel = Variaveis(dialog_id, var_name, var_value)
            db.session.add(nova_variavel)
            db.session.commit()

    def execute(self, chat_id, dialog_id, **kw):
        deal = kw.get('deal', 0)
        if deal:
            campo = self.__get_card(kw.get('deal', 0), self.field)
            print(campo)
        self.__save_var(self.var_name, campo, dialog_id)
        return self.get_proximo_bloco()