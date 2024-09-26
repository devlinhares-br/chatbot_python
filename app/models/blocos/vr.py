from app.models.banco.variaveis import Variaveis
from app import db

class Vr():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, proximo_bloco, var_name, var_value) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.var_name = var_name
        self.var_value = var_value
        self.proximo_bloco = proximo_bloco
    
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
    
    def get_proximo_bloco(self):
        return self.proximo_bloco
    
    def execute(self, chat_id, dialog_id, **kw):
        self.__save_var(self.var_name, self.var_value, dialog_id)
        return self.get_proximo_bloco()
    