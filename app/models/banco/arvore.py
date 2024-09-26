from app import db
from app.models.blocos.start import START
from app.models.blocos.ms import Ms
from app.models.blocos.gt import Gt
from app.models.blocos.op import Op
from app.models.blocos.tr import Tr
from app.models.blocos.vr import Vr
from app.models.blocos.mt import MT
from app.models.blocos._if import IF
from app.models.blocos.ao import Ao
from app.models.blocos.ed import Ed
from app.models.blocos.mc import Mc
from app.models.blocos.gd import Gd
from uuid import uuid4
import json
class Arvore(db.Model):
    __tablename__ = 'arvore'
    uuid = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: uuid4())
    tipo = db.Column(db.String(3), nullable=False)
    identificador = db.Column(db.String(6), nullable=False)
    bloco = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return self.bloco

    def get_uuid(self):
        return self.uuid
    
    def get_identificador(self):
        return self.identificador
    
    def get_bloco(self):
            bloco = self.bloco
            return json.loads(bloco)
    
    def to_dict(self):
        return {
            'uuid': self.get_uuid(),
            'identificador': self.get_identificador(),
            'bloco': self.get_bloco()
        }
    
    def create_object_block(self)->object:
        bloco = self.get_bloco()
        objeto = {
            'STT': START(bloco.get('proximo_bloco')),
            'MSG': Ms(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('mensagens', []), bloco.get('proximo_bloco',''), bloco.get('system_message', 'N') , bloco.get('aguarde')),
            'GET': Gt(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('var_name'), bloco.get('proximo_bloco',''), bloco.get('regex'), bloco.get('mensagem_invalido')),
            'OPC': Op(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('mensagem_erro'), bloco.get('opcoes')),
            'TRS': Tr(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('is_user'), bloco.get('to_id'), bloco.get('mensagem'),bloco.get('proximo_bloco')),
            'VR':  Vr(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('proximo_bloco',''), bloco.get('var_name',''), bloco.get('var_value','')),
            'MT':  MT(bloco.get('id_bloco',''), bloco.get('identeficador',''), bloco.get('id_bloco_anterior',''), bloco.get('proximo_bloco', '')),
            'IF':  IF(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('verdadeiro',''), bloco.get('falso','')),
            'AO':  Ao(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('proximo_bloco','')),
            'END': Ed(bloco.get('id_bloco',''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('encerra_conversa_bitrix',False)),
            'MCD': Mc(bloco.get('id_bloco', ''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('pipe', ''), bloco.get('etapa', ''), bloco.get('proximo_bloco','')),
            'GDF': Gd(bloco.get('id_bloco', ''), bloco.get('identificador',''), bloco.get('id_bloco_anterior',''), bloco.get('var_name', ''), bloco.get('field', ''), bloco.get('proximo_bloco',''))
        }
        return objeto[self.tipo]
    