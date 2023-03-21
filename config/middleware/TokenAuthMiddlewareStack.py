# my_app/token_auth.py

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import close_old_connections
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 3
    """
    def __init__(self, inner, auth_token_key='Authorization'):
        self.inner = inner
        self.auth_token_key = auth_token_key

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        if self.auth_token_key.encode() in headers:
            # Check the token
            try:
                token_name, token_key = headers[self.auth_token_key.encode()].decode().split(' ')
                if token_name.lower() == 'token':
                    token = await database_sync_to_async(Token.objects.get)(key=token_key)
                    scope['user'] = await database_sync_to_async(User.objects.get)(id=token.user_id)
            except (ValueError, Token.DoesNotExist):
                pass

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        return await self.inner(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
