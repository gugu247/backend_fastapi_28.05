#PyJWT pwdlib[argon2] python-multipart
#PyJWT pwdlib python-multipart

import jwt
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

import database_
from schemas import UserProfile
from datetime import timezone,timedelta,datetime

# orig_login = 'Bebeb'
# orig_pass = 'Hehhe'

# user_login = input()
# user_pass = input()

# def func_hash(text:str) -> str:
#     count = 0
#     for i in range(len(text)):
#         count += ord(text[i])
#     return str(count)

# if func_hash(user_login) == func_hash(orig_login) and func_hash(user_pass) == func_hash(orig_pass):
#     print('OK')
# else:
#     print('Error')


# def func_hash(text:str) -> str:
#     count = 0
#     for i in range(len(text)):
#         tmp = ord(text[i])
#         tmpm = i-1
#         tmpp = i+1
#         if tmpm < 0:
#             tmpm = len(text) - 1
#         if tmpp > len(text) - 1:
#             tmpp = 0
#         tmp += ord(text[tmpp]) + ord(text[tmpm])
#         count += int(tmp)
#     return str(count)


SECRET_KEY = 'TUTRANDOMKEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def hash_password(password:str) -> str:
    return password_hash.hash(password)

def verify_password(password:str,password_hash_value:str) -> bool:
    return password_hash.verify(password,password_hash_value)

def authenticate_user(username:str,password:str) -> UserProfile | None:
    user_record = database_.get_user_record_by_username(username)
    if user_record is None:
        return None
    if not verify_password(password, user_record['password_hash']):
        return None
    return UserProfile(
        id=user_record['id'],
        username=user_record['id'],
        role=user_record['role']
    )

def create_access_token(user: UserProfile) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub': str(user.id),
        'exp':expires_at
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

# user_test= UserProfile(id=0,username='LADCLAK',role='LSJK')
# print(create_access_token(user_test))

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserProfile:
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token'
    )
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
        sub=payload.get('sub')
        if not isinstance(sub,str):
            raise token_exception

        user_id = int(sub)
    except (InvalidTokenError, ValueError, TypeError):
        raise token_exception

    user = database_.get_user_by_id(user_id)
    if user is None:
        raise token_exception
    return user

