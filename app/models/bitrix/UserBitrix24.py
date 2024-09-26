from app.models.bitrix.DataUser import DataUser

class UserBitrix24():
    def __init__(self, user:DataUser) -> None:
        self.user = DataUser
        pass

    def get_user_id(self):
        return self.user.id
    
    def get_phone(self):
        return self.user.phones
    
    