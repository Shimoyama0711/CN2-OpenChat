class Room:
    def __init__(self, room_number, amount, time_limit, villager_count, wolf_count, madman_count):
        self.room_number = room_number
        self.players = []  # プレイヤーのリスト
        self.turn = 0  # ターン番号（何日目か）
        self.message_history = []  # 会話履歴
        self.amount = amount  # プレイ人数
        self.time_limit = time_limit  # 議論する時間
        self.villager_count = villager_count  # 村人の人数
        self.wolf_count = wolf_count  # 人狼の人数
        self.madman_count = madman_count  # 狂人の人数

    def add_player(self, player):
        """ プレイヤーを部屋に追加する。
        すでに同じ名前のプレイヤーが存在する場合は追加しない。"""
        for p in self.players:
            if p.name == player.name:
                return
        self.players.append(player)

    def remove_player(self, player_name):
        for p in self.players:
            if p.name == player_name:
                self.players.remove(p)

    def send_message(self, message_data):
        """ 部屋にメッセージを送信する """
        self.message_history.append(message_data)

    def next_turn(self):
        """ 次のターン（日）に進む """
        self.turn += 1

    def add_chat_message(self, message):
        """ チャットメッセージを履歴に追加する """
        self.message_history.append(message)

    def get_chat_history(self):
        """ チャット履歴を取得する """
        return self.message_history

    def __repr__(self):
        return f"Room(room_number='{self.room_number}', players={self.players}, turn={self.turn}, message_history={self.message_history}, amount={self.amount}, time_limit={self.time_limit}, villager_count={self.villager_count}, wolf_count={self.wolf_count}, madman_count={self.madman_count})"

    def __str__(self):
        return f"Room(room_number='{self.room_number}', players={self.players}, turn={self.turn}, message_history={self.message_history}, amount={self.amount}, time_limit={self.time_limit}, villager_count={self.villager_count}, wolf_count={self.wolf_count}, madman_count={self.madman_count})"

