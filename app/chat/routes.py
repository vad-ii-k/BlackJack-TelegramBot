import typing

from app.chat.views import ChatView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view(r"/chat/{chat_id:-?\d+}", ChatView)
