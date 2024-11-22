from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
# from notifications.routing import websocket_urlpatterns  # Ensure this file exists in notifications directory

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AuthMiddlewareStack(  # Handle WebSocket requests
        URLRouter(
            # websocket_urlpatterns  # Defined in notifications.routing
        )
    ),
})
