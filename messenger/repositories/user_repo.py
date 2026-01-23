from messenger.db.models.user import User
from messenger.schemes.user import UserInternal


class UserRepository:


    # initialize current db session
    def __init__(self, db):

        self.db = db


    # Creates new User Entry in user table
    def create_user(self, email : str, hashed_pw : str, user_name : str):
        new_user = User(
            name=user_name,
            email=email,
            password=hashed_pw,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user


    # Return usernames
    def get_user_name(self, id_list : list):
        names = self.db.query(User.name).filter(User.id.in_(id_list)).all()
        return [n[0] for n in names]


    # Return User details via UserID
    def get_user_by_id(self, user_id : int):
        return self.db.query(User).filter(User.id == user_id).first()

    # Return User Details via email
    def get_user_by_email(self, email : str):
        return self.db.query(User).filter(User.email == email).first()

    # Return user Details via username (could be more users than 1)
    def get_user_by_username(self, username : str):
        return self.db.query(User).filter(User.name == username).all()

    # Return all current users
    def get_all_users(self):
        return self.db.query(User).all()


    # Update only given Columns
    def update_user(self, user, user_details : dict):
        for key, value in user_details.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Update the user password after validation
    def update_user_password(self,user : User, new_password : str):
        user.password = new_password
        self.db.commit()
        self.db.refresh(user)
        return user

    # Setting User Status to "Inactive"
    def deactivate_user(self, user : User , user_status : str):
        user.status = user_status
        self.db.commit()
        self.db.refresh(user)
        return user


    # Setting User Status to "active"
    def activate_user(self, user_id : int , user_status):
        user = self.get_user_by_id(user_id)
        user.status = user_status
        self.db.commit()
        self.db.refresh(user)
        return user


