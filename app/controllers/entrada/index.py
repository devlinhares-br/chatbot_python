from app import app, db
from flask import request, jsonify
from app.models.bitrix.DataMessage import DataMessage
from app.controllers.bot import Bot
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

@app.route('/cad/arvore/hlsdkfjghvoikdslfhgkdl', methods=['POST'])
def cad_arvore():
    data = request.get_json()

    arvore = [Arvore(identificador=bloco.get('id_bloco'), tipo=bloco.get('identificador'), bloco= json.dumps(bloco)) for bloco in data]

    db.session.bulk_save_objects(arvore)
    db.session.commit()

    return jsonify({'retorno': f"{len(arvore)} motivos cadastrados com sucesso."})
