import bcrypt


class Hashing:

    @staticmethod
    def hash_password(password):
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_pw.decode('utf-8', errors='ignore')

    @staticmethod
    def check_password(user_pw, db_pw):
        return bcrypt.checkpw(user_pw.encode('utf-8'), db_pw.encode('utf-8'))