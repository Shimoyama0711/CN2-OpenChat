import datetime


class Message:
    def __init__(self, msg, name, avatar, date):
        self.msg = msg
        self.name = name,
        self.avatar = avatar,
        self.date = date

    def to_dict(self):
        """ Messageオブジェクトの状態を辞書型で返す """
        return {
            "msg": self.msg,
            "name": self.name,
            "avatar": self.avatar,
            "date": self.date
        }

    def __repr__(self):
        return f"Message(msg='{self.msg}, name={self.name}, avatar={self.avatar}, date={self.date}')"

    def __str__(self):
        return f"Message(msg='{self.msg}, name={self.name}, avatar={self.avatar}, date={self.date}')"
