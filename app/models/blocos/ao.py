from app.models.banco.variaveis import Variaveis
from app.services.dhl.dhl import DHL
from app import db
from datetime import datetime
import re

class Ao():
    def __init__(self, id_bloco, identificador, id_bloco_anterior, proximo_bloco) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.proximo_bloco = proximo_bloco
        self.dhl = DHL()
    
    def get_proximo_bloco(self):
        return self.proximo_bloco
    
    def execute(self, chat_id, dialog_id, **kw):
        perfil_veiculo = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'perfil_veiculo').first()
        tipo_veiculo = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'tipo_veiculo').first()
        placa_veiculo = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'placa_veiculo').first()
        motivo_ocorrencia = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'motivo_ocorrencia').first()
        nome_motorista = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'nome').first()
        phone = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'phone').first()
        veiculo = self.dhl.get_veiculo(tipo_veiculo.value, perfil_veiculo.value)
        notas = Variaveis.query.filter_by(dialog_id=dialog_id, name='notas').first()
        notas = str(notas.value).split('\n')
        if phone.value is None:
            phone.value = '0'
        msg = ''
        nome_cliente = ''

        for nota in notas:
            
            if not re.findall('^[A-Za-z0-9]+ \d{2}/\d{2}/\d{4}$', nota):
                msg = f'{msg}\nNota: {nota[0]} - Falha ao abrir a ocorrência. Formato inválido!'
                continue

            nota = nota.split(' ')
            
            nota[1] = datetime.strptime(nota[1], "%d/%m/%Y").strftime("%Y-%m-%d")

            ocorrencia = [{
                'nota': nota[0],
                'serie': '15',
                'dataemis': nota[1],
                'motivo_codigo': int(motivo_ocorrencia.value),
                'motorista': nome_motorista.value,
                'placa': ''.join(re.findall(r'\w', placa_veiculo.value)),
                'id_veiculo': veiculo,
                'telefone': re.sub(r'\D', '', phone.value)
            }]

            ocorrencias_abertas = self.dhl.cria_ocorrencia(ocorrencia)
            print(ocorrencias_abertas)
            ocorrencia = None
        
            if 'ocorrencias' in ocorrencias_abertas:
                for ocorrencia in ocorrencias_abertas['ocorrencias']:
                    nome_cliente = ocorrencia.get('nome_cliente')
                    msg = f'{msg}\nNota: {ocorrencia["nota_numero"]} - Ocorrencia: {ocorrencia["ocorrencia"]}'
            else:
                msg = f'{msg}\nNota: {nota[0]} - Falha ao abrir a ocorrência!'
            
        nome_cliente = Variaveis(dialog_id=dialog_id, name = 'nome_cliente', value=nome_cliente)
        lista_ocorrencia = Variaveis(dialog_id=dialog_id, name = 'lista_ocorrencia', value=msg)

        db.session.add(nome_cliente)
        db.session.add(lista_ocorrencia)
        db.session.commit()

        return self.get_proximo_bloco()
    