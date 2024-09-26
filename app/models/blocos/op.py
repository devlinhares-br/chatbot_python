from app.models.bitrix.bitrix import Bitrix

class Op():
    def __init__(self, id_bloco: str, identificador, id_bloco_anterior: str, mensagem_erro: str, opcoes: dict) -> None:
        self.id_bloco = id_bloco
        self.identificador = identificador
        self.id_bloco_anterior = id_bloco_anterior
        self.mensagem = mensagem_erro
        self.opcoes = opcoes
        self.opcao = None
        self.__bitrix = Bitrix()
    
    def __send_menssage(self, dialog_id):
        self.__bitrix.send_menssage(self.mensagem, dialog_id)
    
    def set_opcao(self, opcao):
        if opcao in self.opcoes:
            return self.opcoes[opcao]
        return False
    
    def execute(self, chat_id, dialog_id, **kw):
        opcao_selecionada = self.set_opcao(kw['user_last_message'])
        print('opção selecionada')
        print(opcao_selecionada)
        
        if not opcao_selecionada:
            print('nada selecionado')
            self.__send_menssage(dialog_id)
            return self.id_bloco_anterior
        return opcao_selecionada
