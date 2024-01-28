import datetime


class Message:
    def __init__(self, msg, name, date):
        self.msg = msg
        self.name = name,
        self.date = date

    def __repr__(self):
        return f"Message(msg='{self.msg}, name={self.name}, date={self.date}')"

    def __str__(self):
        return f"Message(msg='{self.msg}, name={self.name}, date={self.date}')"
