from enum import Enum


class CallbackAnswerText(str, Enum):
    MSG_ALREADY_STARTED = "Игра уже идет!"
    MSG_GAME_CREATED = "Игра создана!"
    MSG_JOINED_GAME = "Вы добавлены в игру!"
    MSG_GAME_ENDED = "Игра уже закончена!"
    MSG_ALREADY_PLAYING = "Вы уже в игре!"
    MSG_GAME_STARTED = "Игра началась!"
    MSG_NOT_IN_GAME = "Вы не участвуете в этой игре!"
    MSG_WAIT_FOR_RESULTS = "Ожидайте окончания игры!"
    MSG_ALREADY_MADE_TURN = "Вы уже сделали ход в этом раунде!"
    MSG_HIT = "Вы взяли карту!"
    MSG_STAND = "Вы закончили набор карт!"
    MSG_JOIN_TO_TAKE_PART = "Присоединитесь для участия в игре!"
    MSG_PLACE_BET = "Делайте ставки!"
    MSG_ALREADY_PLACES_BET = "Вы уже сделали ставку!"
    MSG_BID_ACCEPTED = "Ставка принята!"


class Commands(str, Enum):
    START_GAME = "/start_game"
    MY_STATISTICS = "/my_statistics"
    HELP = "/help"


class CallbackData(str, Enum):
    CREATE = "create"
    JOIN = "join"
    START = "start"
    HIT = "hit"
    STAND = "stand"
    BET = "bet"
