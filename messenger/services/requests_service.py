from messenger.repositories.requests_repo import RequestsRepo
from messenger.core.exceptions import RequestExistsError, RequestNotFoundError, RequestBlockedError, FriendshipExistsError, NoRequestsFoundError, SameUserIDError
from messenger.enums import RequestStatus
from messenger.repositories.friends_repo import FriendsRepository
from messenger.repositories.user_repo import UserRepository


class RequestsService:

    def __init__(self, db):

        self.repository = RequestsRepo(db)
        self.friends_repository = FriendsRepository(db)
        self.user_repository = UserRepository(db)


    def create_request(self, send_user_id : int, rec_user_id : int):

        if send_user_id == rec_user_id:
            raise SameUserIDError()

        validate = self.repository.get_request(send_user_id, rec_user_id)
        friendship = self.friends_repository.get_friendship(send_user_id, rec_user_id)

        if validate and not friendship and (validate.status == RequestStatus.ACCEPTED.value or validate.status == RequestStatus.REJECTED.value or validate.status == RequestStatus.REVOKED.value):
            return self.repository.update_request(send_user_id, rec_user_id, RequestStatus.SENT)
        if friendship:
            raise FriendshipExistsError()
        elif validate and validate.status == RequestStatus.BLOCKED.value:
            raise RequestBlockedError()
        elif validate:
            raise RequestExistsError()

        return self.repository.create_request(send_user_id, rec_user_id)


    def get_request_by_id(self, id : int):
        request = self.repository.get_request_by_id(id)
        if not request:
            raise RequestNotFoundError()
        return request

    def get_request(self, send_user_id : int, rec_user_id : int):

        return self.repository.get_request(send_user_id, rec_user_id)

    def get_sent_requests(self, send_user_id : int):

        requests =  self.repository.get_send_request(send_user_id)
        if not requests:
            raise NoRequestsFoundError()
        for request in requests:
            rec_user = self.user_repository.get_user_by_id(request.rec_user_id)
            request.rec_user_name = rec_user.name
        return requests

    def get_rec_requests(self, rec_user_id : int):

        requests = self.repository.get_rec_request(rec_user_id)
        if not requests:
            raise NoRequestsFoundError()
        for request in requests:
            send_user = self.user_repository.get_user_by_id(request.send_user_id)
            request.send_user_name = send_user.name
        return requests

    def get_accepted_requests(self, user_id : int):

        return self.repository.get_accepted_request(user_id)

    def get_blocked_requests(self, user_id : int):

        blocked_requests = self.repository.get_blocked_requests(user_id)
        if not blocked_requests:
            raise NoRequestsFoundError()
        for request in blocked_requests:
            send_user = self.user_repository.get_user_by_id(request.send_user_id)
            request.send_user_name = send_user.name
        return blocked_requests


    def sync_requests(self, user_id : int, last_seen_id : int):
        return self.repository.sync_requests(user_id, last_seen_id)


    def update_request(self, send_user_id : int, rec_user_id : int, status):

        validate = self.repository.get_request(send_user_id, rec_user_id)
        if not validate:
            raise RequestNotFoundError()
        request = self.repository.update_request(send_user_id, rec_user_id, status)
        friendship = None
        if status == RequestStatus.ACCEPTED.value:
            friendship = self.friends_repository.create_friendship(send_user_id, rec_user_id)

        return {"request" : request,
                "friendship" : friendship}


