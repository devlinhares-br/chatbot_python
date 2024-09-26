from app import db
from app.models.banco.arvore import Arvore
from app.models.banco.conversas import Conversas
from app.models.banco.variaveis import Variaveis
from app.models.bitrix.DataMessage import DataMessage
from app.models.blocos.ed import Ed
from app.models.bitrix.bitrix import Bitrix

class Bot():
    def __init__(self, data: DataMessage) -> None:
        self.data = data
        self.__bitrix = Bitrix()
        self.set_arvore()
        
    def set_bloco(self):
        self.bloco_atual = self.conversa.current_block
    
    def get_bloco_atual(self):
        return self.bloco_atual
    
    def set_arvore(self):
        self.arvore = Arvore.query.all()
    
    def get_conversa(self):
        conversa = Conversas.query.filter_by(dialog_id = self.data.params.dialog_id).first()
        
        if conversa:
            self.conversa = conversa
        else:
            self.conversa = Conversas(self.data.params.dialog_id, 'START')
        db.session.commit()
    
    def save_conversa(self, current_block):
        conversa = Conversas.query.filter_by(dialog_id = self.data.params.dialog_id).first()
        if not conversa:
            try:
                self.conversa = Conversas(self.data.params.dialog_id, self.get_bloco_atual())
                self.conversa.set_modified_on()
                db.session.add(self.conversa)
                db.session.commit()
            except ConnectionError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            conversa.current_block = current_block
            self.conversa.set_modified_on()
            Conversas.query.filter_by(dialog_id = self.data.params.dialog_id).update(conversa.to_dict())
            db.session.commit()

    def verify_phone_variable(self, phone_value, dialog_id):
        phone_variables = Variaveis.query.filter_by(dialog_id=dialog_id, name = 'phone').first()
        if phone_variables:
            return True
        else:
            phone = Variaveis(dialog_id=dialog_id, name='phone', value=phone_value)
            db.session.add(phone)
            db.session.commit()
            return True
    
    def list_users_chat(self, chat_id):
        users = self.__bitrix.list_chat_user(chat_id)
        return users
    
    def get_im_user(self, id):
        return self.__bitrix.im_user_get(id)
    
    def save_phone_user(self):
        users = self.list_users_chat(self.data.params.chat_id)

        for user in users:
            if user == 0:
                continue
            data_user = self.get_im_user(user)
            if data_user.id != self.__bitrix.get_bot_id():
                self.verify_phone_variable(data_user.phones.personal_mobile, self.data.params.dialog_id)


    def main(self):
        self.set_arvore()
        self.get_conversa()
        self.set_bloco()
        while True:
            for folha in self.arvore:
                if folha.bloco is None:
                    break
                if self.bloco_atual == folha.identificador:
                    self.bloco_objeto = folha.create_object_block()
                    resultado = self.bloco_objeto.execute(dialog_id = self.data.params.dialog_id, chat_id = self.data.params.chat_id, user_last_message = self.data.params.message, deal = self.conversa.deal)
            print(f'Resultado: {resultado}')
            if resultado == -1:
                return True
            if not resultado:
                if hasattr(self.bloco_objeto, 'proximo_bloco'):
                    self.bloco_atual = self.bloco_objeto.proximo_bloco
                break
            print(resultado)
            self.bloco_atual = resultado
            print(f"{'-=-='*10}")
        if not isinstance(self.bloco_objeto, Ed):
            print(self.bloco_atual)
            self.save_conversa(self.bloco_atual)