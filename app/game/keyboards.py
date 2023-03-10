from dataclasses import dataclass

from app.store.tg_api.dataclassess import InlineKeyboardButton


@dataclass(slots=True, frozen=True)
class GameKeyboard:
    EMPTY = [[]]
    CREATE_GAME = [
        [
            InlineKeyboardButton(
                text="🆕 Начать игру",
                callback_data="create",
            ),
        ]
    ]
    JOIN_GAME = [
        [
            InlineKeyboardButton(
                text="Присоединиться ➕",
                callback_data="join",
            ),
            InlineKeyboardButton(
                text="Все готовы ❕",
                callback_data="start",
            ),
        ]
    ]
    MAKES_TURN = [
        [
            InlineKeyboardButton(
                text="Ещё 🙋",
                callback_data="hit",
            ),
            InlineKeyboardButton(
                text="Хватит 🙅",
                callback_data="stand",
            ),
        ]
    ]
