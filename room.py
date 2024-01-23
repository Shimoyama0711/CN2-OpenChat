class Room:
    def __init__(self, room_number, amount, time_limit, wolf_count):
        self.room_number = room_number
        self.players = []  # プレイヤーのリスト
        self.turn = 0  # ターン番号（何日目か）
        self.chat_history = []  # チャット履歴
        self.amount = amount  # 参加人数
        self.time_limit = time_limit  # 議論する時間
        self.wolf_count = wolf_count  # 人狼の人数

    def add_player(self, player):
        """ プレイヤーを部屋に追加する """
        self.players.append(player)

    def next_turn(self):
        """ 次のターン（日）に進む """
        self.turn += 1

    def add_chat_message(self, message):
        """ チャットメッセージを履歴に追加する """
        self.chat_history.append(message)

    def get_chat_history(self):
        """ チャット履歴を取得する """
        return self.chat_history