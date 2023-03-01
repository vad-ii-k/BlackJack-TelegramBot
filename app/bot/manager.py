import typing
from logging import getLogger

from app.store.tg_api.dataclassess import (
    AnswerCallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            if update.message:
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            text="click",
                            callback_data="{'button': 'click'}",
                        ),
                    ]
                ]
                await self.app.store.tg_api.send_message(
                    message=Message(
                        chat=update.message.chat,
                        text=update.message.from_user.first_name,
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=inline_keyboard,
                        ),
                    )
                )
            elif update.my_chat_member:
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            text="Начать игру",
                            callback_data="{'button': 'start'}",
                        ),
                    ]
                ]
                await self.app.store.tg_api.send_message(
                    message=Message(
                        chat=update.my_chat_member.chat,
                        text="Привет, я BlackJack бот!",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=inline_keyboard
                        ),
                    )
                )
            elif update.callback_query:
                await self.app.store.tg_api.answer_callback_query(
                    answer=AnswerCallbackQuery(
                        id=update.callback_query.id,
                        text="Вы нажали на кнопку",
                    )
                )
                await self.app.store.tg_api.edit_message(
                    message=Message(
                        chat=update.callback_query.message.chat,
                        text=update.callback_query.message.text
                        + "\n"
                        + update.callback_query.from_user.first_name,
                        message_id=update.callback_query.message.message_id,
                        reply_markup=update.callback_query.message.reply_markup,
                    )
                )
