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
    PLACE_BET = [
        [
            InlineKeyboardButton(
                text="100 💲",
                callback_data=f"{CallbackData.BET.value}:100",
            ),
            InlineKeyboardButton(
                text="200 💲",
                callback_data=f"{CallbackData.BET.value}:200",
            ),
            InlineKeyboardButton(
                text="400 💲",
                callback_data=f"{CallbackData.BET.value}:400",
            ),
            InlineKeyboardButton(
                text="800 💲",
                callback_data=f"{CallbackData.BET.value}:800",
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
