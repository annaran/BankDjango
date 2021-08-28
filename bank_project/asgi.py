import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import bank_app.routing
import customer_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bank_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            customer_app.routing.websocket_urlpatterns,
        )
    ),
})
