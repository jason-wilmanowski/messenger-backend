import jwt
from messenger.core.config import settings as config
from datetime import datetime, timedelta
from messenger.core.exceptions import TokenError


# Access Token Section

def create_access_token(user_id : int):
        payload = {}
        payload['iat'] = datetime.utcnow()
        payload['exp'] = (datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRES))
        payload['sub'] = str(user_id)
        token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return token

def decode_access_token(token):
        try:
            payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])

            user_id = payload.get('sub')
            if user_id is None:
                raise TokenError("Invalid token payload")

            return int(user_id)

        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired")

        except jwt.InvalidTokenError:
            raise TokenError("Invalid token")



# Refresh Token Section

def create_refresh_token(user_id : int):

        payload = {}
        payload['sub'] = str(user_id)
        payload['exp'] = datetime.utcnow() + timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRES)
        payload['iat'] = datetime.utcnow()
        payload['type'] = "refresh"
        token = jwt.encode(payload, config.JWT_REFRESH_SECRET_KEY, algorithm=config.JWT_REFRESH_ALGORITHM)
        return token

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, config.JWT_REFRESH_SECRET_KEY, algorithms=[config.JWT_REFRESH_ALGORITHM])
        user_id = payload.get('sub')

        if user_id is None:
            raise TokenError("Invalid token payload")
        if payload['type'] != "refresh":
            raise TokenError("Invalid token type")

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise TokenError("Token expired")
    except jwt.InvalidTokenError:
        raise TokenError("Invalid token")