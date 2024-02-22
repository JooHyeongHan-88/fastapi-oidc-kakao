# from tinydb import TinyDB, Query


# class UserModel:

#     def __init__(self, path='db.json'):
#         self.db = TinyDB(path)

#     def upsert_user(self, user):
#         if not self.db.search(Query().id == user.id):
#             self.db.insert(user.serialize())

#     def get_user(self, user_id):
#         user = self.db.search(Query().id == user_id)
#         return UserData.deserialize(user[0])

#     def remove_user(self, user_id):
#         self.db.remove(Query().id == user_id)


class UserData:
    
    def __init__(self, userinfo=None):
        if userinfo:
            self.nickname = userinfo['nickname']
            self.picture = userinfo['picture'] 
        else:
            self.nickname = None
            self.picture = None

    def __str__(self):
        return f"<UserData>(nickname:{self.nickname})"

    def serialize(self):
        return {
            "nickname": self.nickname,
            "picture": self.picture,
        }

    @staticmethod
    def deserialize(userinfo):
        user = UserData()
        user.nickname = userinfo['nickname']
        user.picture = userinfo['picture']
        return user