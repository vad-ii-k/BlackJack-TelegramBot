from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.admin.routes import setup_routes as admin_setup_routes
    from app.chat.routes import setup_routes as chat_setup_routes
    from app.player.routes import setup_routes as player_setup_routes

    admin_setup_routes(app)
    player_setup_routes(app)
    chat_setup_routes(app)
