from messenger.db.models.friends import Friend
from sqlalchemy import or_, and_

class FriendsRepository:

    # initialize DB session
    def __init__(self, db):

        self.db = db


    # Creates new friendship entry
    def create_friendship(self, user_id_1: int, user_id_2: int):

        new_friendship = Friend(user_id_1=user_id_1, user_id_2=user_id_2)

        self.db.add(new_friendship)
        self.db.commit()
        self.db.refresh(new_friendship)
        return new_friendship


    # to validate uniqueness before creating new friendship
    def get_friendship(self, user_id_1: int, user_id_2: int):
        friendship = self.db.query(Friend).filter(or_(and_(Friend.user_id_1 == user_id_1, Friend.user_id_2 == user_id_2),
                                                      and_(Friend.user_id_1 == user_id_2, Friend.user_id_2 == user_id_1))).first()
        return friendship

    # get all friends from a user
    def get_friends(self, user_id: int):
        user_friends = self.db.query(Friend).filter(or_(Friend.user_id_1 == user_id,
                                                        Friend.user_id_2 == user_id)).all()
        return user_friends


    # delete friendship between 2 users
    def delete_friendship(self, user_id_1: int, user_id_2: int):
        friendship = self.get_friendship(user_id_1, user_id_2)
        self.db.delete(friendship)
        self.db.commit()

        return friendship
