#PyJWT pwdlib[argon2] python-multipart

import jwt
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from schemas import UserProfile

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

def auth_user(username:str,password:str) -> UserProfile | None:
    pass