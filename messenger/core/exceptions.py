

# General Error Exceptions
class NotAllowedError(Exception):
    pass




# Token Exception for JWT decode_access_token
class TokenError(Exception):
    pass


# Auth Exceptions used in Auth service layer
class InvalidPasswordError(Exception):
    pass


# User Error in User Service Layer
class UserExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserSameStatusError(Exception):
    pass

class SameUserIDError(Exception):
    pass


# Conversation Error in Conversation Service layer
class ConversationExistsError(Exception):
    pass

class ConversationNotFoundError(Exception):
    pass


# Message Error in Message Service layer
class MessageNotFoundError(Exception):
    pass

class NoMessagesFoundError(Exception):
    pass

class MessageInvalidError(Exception):
    pass

class MessageAlreadyDeletedError(Exception):
    pass



# Friends Error in Friends Service layer
class FriendshipExistsError(Exception):
    pass

class FriendshipNotFoundError(Exception):
    pass

class NoFriendsFoundError(Exception):
    pass


# Requests Error in Requests Service layer
class RequestExistsError(Exception):
    pass

class RequestNotFoundError(Exception):
    pass

class RequestBlockedError(Exception):
    pass

class NoRequestsFoundError(Exception):
    pass
