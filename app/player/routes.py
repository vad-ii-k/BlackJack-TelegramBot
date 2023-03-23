import typing

from app.player.views import PlayerView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view(r"/player/{tg_id:\d+}", PlayerView)
