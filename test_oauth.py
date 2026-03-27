import os
from services.google_oauth import build_auth_url
try:
    print(build_auth_url(state='test', redirect_uri='http://192.168.1.100:8000/auth/google/callback'))
except Exception as e:
    print('ERROR:', type(e), e)