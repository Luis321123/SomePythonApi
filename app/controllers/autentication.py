from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.settings import get_settings
from fastapi import HTTPException, Request
from datetime import datetime
import jwt
import requests as rq

 
settings = get_settings()

jwt_secret = settings.JWT_SECRET
jwt_algorithm = settings.JWT_ALGORITHM
auth_url = settings.AUTH_URL


def decodeJWT(token: str):
  try:
    decode_token = jwt.decode(token, jwt_secret, algorithms=jwt_algorithm)
    return decode_token
  except:
    return None
  
class jwtBearer(HTTPBearer):

  get_user:bool = False
  get_data:bool = False
  get_token:bool = False

  def __init__(self, auto_Error : bool = True, get_user:bool = False, get_data:bool = False, get_token:bool = False):
    super(jwtBearer, self).__init__(auto_error=auto_Error)
    self.get_user = get_user
    self.get_data = get_data
    self.get_token = get_token

  async def __call__(self, request : Request):
    credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
    
    session = self.verify_jwt(credentials.credentials)
    
    if not session:
      print('not executed')
      print(session)
      raise HTTPException(status_code=401, detail="Invalid or expired token   .")
    

    if self.get_user:
      header = {"authorization":f"Bearer {credentials.credentials}"}
      resp = rq.get(headers=header, url=auth_url + "/user/my_profile")
      return resp.json()

    if self.get_data:
      return session
    
    if self.get_token:
      return credentials.credentials
      
  def verify_jwt(self, jwtoken:str):
    token = decodeJWT(token=jwtoken)

    if not token:
        return False

    if datetime.strptime(token['expiry'], '%y-%m-%d %H:%M:%S') > datetime.now():
        return token
    else:
        print('expired')
        return False