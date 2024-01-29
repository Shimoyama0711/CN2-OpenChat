import base64


class Player:
    def __init__(self, name, avatar, role):
        self.name = name  # 名前
        self.avatar = avatar  # Base64エンコード済みのアバター画像
        self.role = role  # 役職（例：'villager', 'werewolf', 'seer' など）
        self.is_alive = True  # 生存状態（初期状態では生きている）
        self.is_owner = False  # オーナーかどうか

    def die(self):
        """ プレイヤーを死亡状態にする """
        self.is_alive = False

    def revive(self):
        """ プレイヤーを生存状態に戻す（ゲームによっては使用しない） """
        self.is_alive = True

    def get_avatar(self):
        """ Base64エンコードされたアバター画像をデコードして返す """
        return base64.b64decode(self.avatar)

    def __repr__(self):
        return f"Player(name='{self.name}', avatar='{self.avatar}', role='{self.role}', is_alive={self.is_alive}, is_owner={self.is_owner})"

    def __str__(self):
        return f"Player(name='{self.name}', avatar='{self.avatar}', role='{self.role}', is_alive={self.is_alive}, is_owner={self.is_owner})"

    def to_dict(self):
        """ Playerオブジェクトの状態を辞書型で返す """
        return {
            "name": self.name,
            "avatar": self.avatar,
            "role": self.role,
            "is_alive": self.is_alive,
            "is_owner": self.is_owner
        }
