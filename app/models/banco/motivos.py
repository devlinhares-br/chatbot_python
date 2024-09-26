from app import db
from uuid import uuid4

class Motivos(db.Model):
    __tablename__ = 'motivos'
    uuid = db.Column(db.String(36), primary_key=True, unique=True, default=lambda:uuid4())
    motivo_id = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    
    def __init__(self, motivo_id, motivo) -> None:
        super().__init__()
        self.motivo_id = motivo_id
        self.motivo = motivo

    def __repr__(self) -> str:
        return f"{self.motivo_id} - {self.motivo}"
    
    def get_uuid(self):
        return self.uuid

    def to_dict(self):
        return {
            'uuid': self.get_uuid(),
            'motivo_id': self.motivo_id,
            'motivo': self.motivo
        }