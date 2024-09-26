class DataUser():
    def __init__(self, data:dict) -> None:
        self.id = data.get('id', None)
        self.active = data.get('acitive', 0)
        self.name = data.get('name', None)
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        self.work_position = data.get('work_position', None)
        self.avatar = data.get('avatar', None)
        self.gender = data.get('gender', None)
        self.birthday = data.get('birthday', None)
        self.extranet = data.get('extranet', 0)
        self.network = data.get('network', None)
        self.bot = data.get('bot', None)
        self.connector = data.get('connector', 0)
        self.status = data.get('status', None)
        if isinstance(data.get('phones', {}), bool):
            self.phones = DataUserPhone({})
        else:
            self.phones = DataUserPhone(data.get('phones', {}))
        pass


class DataUserPhone():
    def __init__(self, data:dict) -> None:
        self.personal_mobile = data.get('personal_mobile', None)
        self.work_phone = data.get('work_phone', None)
        self.inner_phone = data.get('inner_phone', None)
        pass