import os
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt.middleware import JwtAuthMiddlewareStack
from channels_auth_token_middlewares.middleware import QueryStringSimpleJWTAuthTokenMiddleware
import khatma.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khatamat_b.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # change to uuid method for more security : to be rethinked ...
    # uuid => JwtAuthMiddlewareStack
    # we use this just for rapid connections 
    'websocket': QueryStringSimpleJWTAuthTokenMiddleware(
        URLRouter(khatma.routing.urlpatterns)
    )
})
