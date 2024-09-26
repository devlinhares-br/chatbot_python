from app import db
from app.models.banco.variaveis import Variaveis
from app.services.tratamentos.tratamentos import select_motivo

class MT():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, proximo_bloco) -> None:
        self.id_bloco = id_bloco
        self.id_bloco_anterior = id_bloco_anterior
        self.identificador = identificador
        self.proximo_bloco = proximo_bloco


    def lista_motivos(self, motivo)->list:
        motivos = select_motivo(motivo)
        return motivos[:5]
    
    def cria_msg_motivos(self, motivos:list):
        return '\n'.join(f'{motivo["motivo_id"]} - {motivo["motivo"]}' for motivo in motivos)

    def save_message(self, dialog_id, msg)->None:
        lista_motivos = Variaveis.query.filter_by(dialog_id=dialog_id, name='lista_motivos').first()
        if lista_motivos:
            lista_motivos.value = msg
            Variaveis.query.filter_by(dialog_id=dialog_id, name='lista_motivos').update(lista_motivos.to_dict())
        else:
            lista_motivos = Variaveis(dialog_id, 'lista_motivos', msg)
            db.session.add(lista_motivos)
        db.session.commit()

    def execute(self, chat_id, dialog_id, **kw):
        motivos_lista = self.lista_motivos(kw['user_last_message'])
        msg = self.cria_msg_motivos(motivos_lista)
        self.save_message(dialog_id, msg)
        return self.proximo_bloco
