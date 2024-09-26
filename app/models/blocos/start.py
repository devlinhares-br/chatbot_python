class START():
    def __init__(self, proximo_bloco) -> None:
        self.id_bloco = 'START'
        self.identificador = 'STT'
        self.proximo_bloco = proximo_bloco
    
    def __dict__(self):
        return {
            'id_bloco': self.id_bloco,
            'identificador': self.identificador,
            'proximo_bloco': self.proximo_bloco
        }
    
    def to_dict(self):
        return {
            'id_bloco': self.id_bloco,
            'identificador': self.identificador,
            'proximo_bloco': self.proximo_bloco
        }

    def execute(self, chat_id, dialog_id, **kw):
        return self.proximo_bloco