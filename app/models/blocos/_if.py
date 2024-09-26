from app.models.banco.variaveis import Variaveis

class IF():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, verdadeiro, falso) -> None:
        self.id_bloco = id_bloco
        self.id_bloco_anterior = id_bloco_anterior
        self.identificador = identificador
        self.verdadeiro = verdadeiro
        self.falso = falso
        self.proximo_bloco = ''
    

    def get_variable(self, dialog_id, var:str = 'motivo_ocorrencia')-> Variaveis:
        return Variaveis.query.filter_by(dialog_id=dialog_id, name=var).first()
        
    def validate(self, var)->None:
        print(var)
        print(type(var))
        if var != '0':
            self.proximo_bloco = self.verdadeiro
        else:
            self.proximo_bloco = self.falso

    def execute(self, chat_id, dialog_id, **kw):
        self.validate(kw['user_last_message'])
        return self.proximo_bloco
