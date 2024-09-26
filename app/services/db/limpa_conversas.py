from app.models.banco.conversas import Conversas
from app.models.banco.variaveis import Variaveis
from app.models.bitrix.bitrix import Bitrix
from app.models.bitrix.user_list import UserList
from app import app
import threading
from time import sleep
from datetime import timedelta, datetime

class Ausencia():
    def __init__(self, db : object, interval:int = 60) -> None:
        """LimpaConversas

        Args:
            db (object): Objeto do Banco de dados
            interval (inte): Intervalo de verificação
        """
        self.interval = interval
        self.db = db
        pass

    def delet_conversas(self) -> bool:
        now = datetime.now()
        interval = (now - timedelta(minutes=self.interval))
        bitrix = Bitrix()
        try:

            conversas_para_deletar = Conversas.query.filter(Conversas.modified_on <= interval).all()
            
            if not conversas_para_deletar:
                return True

            for conversa in conversas_para_deletar: 
                Variaveis.query.filter_by(dialog_id=conversa.dialog_id).delete()

            for conversa in conversas_para_deletar:
                self.db.session.delete(conversa)
                bitrix.send_menssage("Estou finalizando a sua conversa por falta de interação!", conversa.dialog_id)
                chat_id = conversa.dialog_id[4:]
                bitrix.end_conversation(chat_id)
            self.db.session.commit()

            return True

        except Exception as err:
            print(err)
            self.db.session.rollback()
            return False
        
    def send_message(self, time = 10):
        now = datetime.now()
        interval = (now - timedelta(minutes=time))
        bitrix = Bitrix()
        try:
            conversas = Conversas.query.filter(Conversas.modified_on <= interval).all()
            for conversa in conversas:
                if self.verifica_conversa_aberta_com_bot(conversa.dialog_id):
                    bitrix.send_menssage("Você ainda está ai?", conversa.dialog_id)
            return True
        
        except Exception as err:
            print(err)
            return False
    
    def verifica_conversa_aberta_com_bot(self, dialog_id):
        bitrix = Bitrix()
        chat = bitrix.list_dialog_user(dialog_id)
        total = int(chat.get('total', 0))
        if total:
            for user in chat['result']:
                user = UserList(user)
                if user.bot:
                    return True
        return False

    def run(self):
        while True:
            with app.app_context():
                sleep(timedelta(minutes=20).seconds)
                if self.delet_conversas():
                    print('ok')
                else:
                    print('ko')
                self.send_message()
                

    def init_task(self):
        task_thread = threading.Thread(target=self.run)
        task_thread.daemon = True
        task_thread.start()
        return True