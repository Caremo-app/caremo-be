from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

import os

# Load config
config = Config(environ={
    "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
    "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
})

# OAUTH
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
    
    # access_token_url='https://oauth2.googleapis.com/token',
    # access_token_params=None,
    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    # authorize_params=None,
    # api_base_url='https://www.googleapis.com/oauth2/v2/',
    # userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
    # jwks_uri=os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL")
)
