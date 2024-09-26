class UserList():
    def __init__(self, user:dict) -> None:
        self.id = user.get('id', 0)
        self.active = user.get('active', False)
        self.name = user.get('name', '')
        self.last_name = user.get('last_name', '')
        self.extranet = user.get('extranet', False)
        self.bot = user.get('bot', False)
        self.connector = user.get('connector', False)
