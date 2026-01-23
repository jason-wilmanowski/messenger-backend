from messenger.db.models.requests import Request
from messenger.enums import RequestStatus
from sqlalchemy import or_, and_

class RequestsRepo:

    # Initialize DB Session
    def __init__(self, db):
        self.db = db


    # creates new friend request entry
    def create_request(self, send_user_id:int, rec_user_id:int):
        new_request = Request(send_user_id=send_user_id, rec_user_id=rec_user_id)
        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)
        return new_request


    # get request by request id
    def get_request_by_id(self, id:int):
        return self.db.query(Request).filter(Request.id == id).first()

    # runs before every create call to validate the uniqueness
    def get_request(self, send_user_id, rec_user_id):
        request = self.db.query(Request).filter(and_(Request.send_user_id == send_user_id,
                                                Request.rec_user_id == rec_user_id)).first()
        return request

    # get all sent requests via UserID
    def get_send_request(self, send_user_id:int):
        requests = self.db.query(Request).filter(and_(Request.send_user_id == send_user_id,
                                                      Request.status == RequestStatus.SENT)).all()
        return requests

    # get all received requests view UserID
    def get_rec_request(self, rec_user_id:int):
        requests = self.db.query(Request).filter(and_(Request.rec_user_id == rec_user_id,
                                                      Request.status == RequestStatus.SENT)).all()
        return requests

    # get all accepted requests via UserID
    def get_accepted_request(self, user_id:int):
        requests = self.db.query(Request).filter(or_(Request.send_user_id == user_id,
                                                 Request.rec_user_id == user_id)).all()
        return requests


    # get all blocked users from requests
    def get_blocked_requests(self, user_id : int):
        return self.db.query(Request).filter(and_(Request.rec_user_id == user_id,
                                                  Request.status == RequestStatus.BLOCKED)).all()


    # sync all requests with id higher than last seen id
    def sync_requests(self, user_id : int, last_seen_id : int):
        return self.db.query(Request).filter(and_(Request.rec_user_id == user_id,
                                                  Request.id > last_seen_id)).all()


    # Updating the friend requests status
    def update_request(self, send_user_id:int, rec_user_id:int, request_status:str):
        request = self.db.query(Request).filter(and_(Request.send_user_id == send_user_id,
                                                Request.rec_user_id == rec_user_id)).first()
        request.status = request_status
        self.db.commit()
        self.db.refresh(request)
        return request

