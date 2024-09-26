from app import db
from uuid import uuid4
from datetime import datetime

class Conversas(db.Model):
    __tablename__ = 'conversas'
    uuid = db.Column(db.String(36), primary_key=True, unique=True, default=lambda:uuid4())
    dialog_id = db.Column(db.String(10), unique=True, nullable=False)
    current_block = db.Column(db.String(6), nullable=False)
    deal = db.Column(db.Integer, nullable=True)
    started_on = db.Column(db.DateTime, default=lambda: datetime.now())
    modified_on = db.Column(db.DateTime, default=lambda: datetime.now())

    def __init__(self, dialog_id, current_block) -> None:
        super().__init__()
        self.dialog_id = dialog_id
        self.current_block = current_block

    def __repr__(self) -> str:
        return f"{self.dialog_id} - {self.current_block}"
    
    def get_uuid(self):
        return self.uuid

    def to_dict(self):
        return {
            'uuid': self.get_uuid(),
            'dialog_id': self.dialog_id,
            'current_block': self.current_block,
            'started_on': self.started_on,
            'modified_on': self.modified_on
        }
    
    def format_(self, date):
        return datetime.strftime(date, '%d/%m/%Y %H:%M')
    
    def set_modified_on(self):
        self.modified_on = datetime.now()
    
    
    def get_stardet_on(self):
        return self.started_on