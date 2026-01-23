from enum import StrEnum


# User account stati
class UserStatus(StrEnum):

    # If User account is active
    ACTIVE = 'active'

    # if User account is inactive (soft delete)
    INACTIVE = 'inactive'



# Friend Request Stati
class RequestStatus(StrEnum):

    # User Accepted Friend Request
    ACCEPTED = 'accepted'

    # User Rejected Friend Request
    REJECTED = 'rejected'

    # Request is sent and stored in database but not delivered to the destination client
    SENT = 'sent'

    # Sending User getting blocked
    BLOCKED = 'blocked'

    # Sending user revoked the pending request
    REVOKED = 'revoked'


# Message Stati
class MessageStatus(StrEnum):

    # Message was sent to the server but not to the destination
    SENT = "sent"

    # Message was delivered to destination
    DELIVERED = "delivered"

    # User read the message
    READ = "read"

    # User deleted his message
    DELETED = "deleted"






