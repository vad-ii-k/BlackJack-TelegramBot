from dataclasses import dataclass

from app.game.enums import CallbackData
from app.store.tg_api.dataclassess import InlineKeyboardButton


@dataclass(slots=True, frozen=True)
class GameKeyboard:
    EMPTY = [[]]
    CREATE_GAME = [
        [
            InlineKeyboardButton(
                text="🆕 Начать игру",
                callback_data=CallbackData.CREATE,
            ),
        ]
    ]
    JOIN_GAME = [
        [
            InlineKeyboardButton(
                text="Присоединиться ➕",
                callback_data=CallbackData.JOIN,
            ),
            InlineKeyboardButton(
                text="Все готовы ❕",
                callback_data=CallbackData.START,
            ),
        ]
    ]
    MAKES_TURN = [
        [
            InlineKeyboardButton(
                text="Ещё 🙋",
                callback_data=CallbackData.HIT,
            ),
            InlineKeyboardButton(
                text="Хватит 🙅",
                callback_data=CallbackData.STAND,
            ),
        ]
    ]
