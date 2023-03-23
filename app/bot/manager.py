import typing
from logging import getLogger

from app.game.handlers import (
    handle_callback_query,
    handle_message,
    handle_my_chat_member,
)
from app.store.tg_api.dataclassess import Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    @staticmethod
    async def handle_updates(updates: list[Update]):
        for update in updates:
            if update.message:
                await handle_message(update.message)
            elif update.my_chat_member:
                await handle_my_chat_member(update.my_chat_member)
            elif update.callback_query:
                await handle_callback_query(update.callback_query)
