from app import db
from uuid import uuid4

class Variaveis(db.Model):
    __tablename__ = 'variaveis'
    uuid = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: uuid4())
    dialog_id = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Text)

    def __init__(self, dialog_id, name, value) -> None:
        self.dialog_id = dialog_id
        self.name = name
        self.value = value
        super().__init__()

    def __repr__(self) -> str:
        return f'{self.name}: {self.value}'
    
    def get_uuid(self):
        return self.uuid
    
    def to_dict(self):
        return {
            'uuid': self.uuid,
            'dialog_id': self.dialog_id,
            'name': self.name,
            'value': self.value
        }
    
    def var_to_dict(self):
        return {
            f'{self.name}': f'{self.value}'
        }