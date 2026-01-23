from messenger.repositories.friends_repo import FriendsRepository
from messenger.core.exceptions import FriendshipExistsError, FriendshipNotFoundError, NoFriendsFoundError
from messenger.repositories.user_repo import UserRepository
from messenger.schemes.friend import FriendsOutput, FriendsItem


class FriendsService:

    def __init__(self, db):

        self.repository = FriendsRepository(db)
        self.user_repository = UserRepository(db)


    def get_friends_name(self, friend_id_list : list):

        names = self.user_repository.get_user_name(friend_id_list)
        return names

    def create_friend(self, user_id_1 : int, user_id_2 : int):

        validate = self.repository.get_friendship(user_id_1, user_id_2)
        if validate:
            raise FriendshipExistsError()
        return self.repository.create_friendship(user_id_1, user_id_2)

    def get_friends(self, user_id : int):

        friends = self.repository.get_friends(user_id)
        if not friends:
            raise NoFriendsFoundError()
        friends_id_list = []
        for friend in friends:
            if friend.user_id_1 != user_id:
                friends_id_list.append(friend.user_id_1)
            else:
                friends_id_list.append(friend.user_id_2)

        friend_names = self.get_friends_name(friends_id_list)
        friend_items = [
            FriendsItem(username=name, id=idu)
            for name, idu in zip(friend_names, friends_id_list)
        ]

        return friend_items


    def get_friendship(self, user_id_1 : int, user_id_2 : int):
        friendship =  self.repository.get_friendship(user_id_1, user_id_2)
        if not friendship:
            raise FriendshipNotFoundError()


    def delete_friendship(self, user_id_1 : int, user_id_2 : int):
        validate = self.repository.get_friendship(user_id_1, user_id_2)
        if not validate:
            raise FriendshipNotFoundError()
        return self.repository.delete_friendship(user_id_1, user_id_2)