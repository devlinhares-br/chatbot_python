from app import app, db
from flask import request, jsonify
from app.models.bitrix.DataMessage import DataMessage
from app.controllers.bot import Bot
from app.models.banco.motivos import Motivos
from app.models.banco.arvore import Arvore
from app.models.banco.conversas import Conversas
from app.models.bitrix.bitrix import Bitrix
from time import sleep
import json

@app.route('/controlador', methods=['POST'])
def controlador():
    dados = request.form.to_dict()
    data_menssage = DataMessage(dados)
    bot = Bot(data_menssage)
    if data_menssage.event == 'ONIMBOTJOINCHAT':
        bot.save_phone_user()
    else: 
        bot.main()
    return jsonify({'status': 'ok', 'return': dados})

@app.route('/status', methods=['GET'])
def status_get():
    return jsonify({
        'status': 200
    })

@app.route('/cad/motivos/hlsdkfjghvoikdslfhgkdl', methods=['POST'])
def cad_motivos():
    data = request.get_json()

    motivos = [Motivos(motivo_id=motivo.get('motivo_id'), motivo=motivo.get('motivo')) for motivo in data]

    db.session.bulk_save_objects(motivos)
    db.session.commit()

    return jsonify({'retorno': f"{len(motivos)} motivos cadastrados com sucesso."})

@app.route('/cad/arvore/hlsdkfjghvoikdslfhgkdl', methods=['POST'])
def cad_arvore():
    data = request.get_json()

    arvore = [Arvore(identificador=bloco.get('id_bloco'), tipo=bloco.get('identificador'), bloco= json.dumps(bloco)) for bloco in data]

    db.session.bulk_save_objects(arvore)
    db.session.commit()

    return jsonify({'retorno': f"{len(arvore)} motivos cadastrados com sucesso."})


@app.route('/controlador/deal', methods=['POST'])
def controlador_deal():
    dados = request.form.to_dict()
    print(dados)
    deal = dados.get('data[FIELDS][ID]')
    bitrix = Bitrix()
    sleep(10)
    conversa = bitrix.crm_chat_get('deal', deal)
    if conversa[0]:
        result = conversa[1]['result']
        for r in result:
            chat_id = r.get('CHAT_ID')
            break
        conversa = Conversas.query.filter_by(dialog_id=f'chat{chat_id}').first()
        conversa.deal = deal
        db.session.add(conversa)
        db.session.commit()
    
    return jsonify({'status': 'ok', 'return': dados})
