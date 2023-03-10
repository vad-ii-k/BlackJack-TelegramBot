import asyncio
from enum import Enum

from app.game.keyboards import GameKeyboard
from app.game.states import PlayerState
from app.game.utils import deal_cards, finish_game, players_roster
from app.store.tg_api.dataclassess import CallbackQuery, Chat, Message, User
from app.web.app import app


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


async def create_game(message: Message) -> str:
    game = await app.store.game.get_active_game(message.chat.id)
    if game:
        return CallbackAnswerText.MSG_ALREADY_STARTED

    await app.store.game.create_game(message.chat.id)

    message.text = "Ожидаем игроков...\n"
    message.reply_markup.inline_keyboard = GameKeyboard.JOIN_GAME
    await app.store.tg_api.edit_message(message)

    return CallbackAnswerText.MSG_GAME_CREATED


async def join_game(callback_query: CallbackQuery) -> str:
    message, user = callback_query.message, callback_query.from_user

    player = await app.store.game.get_player(user.id)
    if player is None:
        player = await app.store.game.create_player(user.id, user.first_name)

    if player.state:
        return CallbackAnswerText.MSG_ALREADY_PLAYING

    game = await app.store.game.get_active_game(message.chat.id)
    if not game:
        return CallbackAnswerText.MSG_GAME_ENDED

    await app.store.game.add_player_to_game(player, game_id=game.id)
    game = await app.store.game.get_active_game(message.chat.id)
    message.text = f"Ожидаем игроков...\nㅤ\n{players_roster(game)}"
    await app.store.tg_api.edit_message(message)
    return CallbackAnswerText.MSG_JOINED_GAME


async def start_game(message: Message) -> str:
    game = await app.store.game.get_active_game(message.chat.id)
    if not game:
        return CallbackAnswerText.MSG_GAME_ENDED

    await deal_cards(game)
    message.reply_markup.inline_keyboard = GameKeyboard.MAKES_TURN
    asyncio.create_task(waiting_for_players_to_turn(message))
    return CallbackAnswerText.MSG_GAME_STARTED


async def makes_turn(
    callback_query: CallbackQuery, new_state: PlayerState
) -> str:
    player = await app.store.game.get_player(callback_query.from_user.id)
    if not player:
        return CallbackAnswerText.MSG_NOT_IN_GAME
    elif player.state == PlayerState.waiting_for_results:
        return CallbackAnswerText.MSG_WAIT_FOR_RESULTS
    elif player.state == PlayerState.waiting_for_hand:
        return CallbackAnswerText.MSG_ALREADY_MADE_TURN
    await app.store.game.update_player(player, new_state)
    if new_state == PlayerState.waiting_for_hand:
        return CallbackAnswerText.MSG_HIT
    else:
        return CallbackAnswerText.MSG_STAND


async def waiting_for_players_to_turn(message: Message, round_num: int = 1):
    game = await app.store.game.get_active_game(message.chat.id)
    message.text = f"{round_num} раунд!\nㅤ\n" + players_roster(game, True)
    await app.store.tg_api.edit_message(message)

    for _ in range(5):
        if all(pl.state != PlayerState.makes_turn for pl in game.players):
            break
        await asyncio.sleep(2)
        game = await app.store.game.get_active_game(message.chat.id)

    for player in game.players:
        if player.state == PlayerState.makes_turn:
            await app.store.game.update_player(
                player, PlayerState.waiting_for_results
            )

    game = await app.store.game.get_active_game(message.chat.id)
    if any(pl.state == PlayerState.waiting_for_hand for pl in game.players):
        await deal_cards(game)
        await waiting_for_players_to_turn(message, round_num + 1)

    elif all(pl.state != PlayerState.makes_turn for pl in game.players):
        await finish_game(game, message)


async def send_player_stats(tg_user: User, chat: Chat):
    stats = await app.store.game.get_player_statistics(tg_user.id)
    if not stats:
        msg = (
            "Вы ни разу не играли со мной☹️\n"
            "Нажмите /start_game, чтобы это исправить)"
        )
        await app.store.tg_api.send_message(
            message=Message(chat=chat, text=msg)
        )
        return

    mention = f"<a href='tg://user?id={tg_user.id}'>{tg_user.first_name}</a>"
    msg = f"Игрок: {mention}\nㅤ\n"
    msg += f"😎 <u>Сыграно игр</u>: {stats.games_played}\n"
    msg += f"🤑 Победы: {stats.games_won}\n"
    msg += f"😡 Поражения: {stats.games_lost}\n"
    draws = stats.games_played - stats.games_won - stats.games_lost
    msg += f"🤗 Ничьи: {draws}\nㅤ\n"
    win_rate = stats.games_won / stats.games_played * 100
    msg += f"📊 Процент побед: {win_rate:.2f}%"

    await app.store.tg_api.send_message(message=Message(chat=chat, text=msg))


async def send_rules(chat: Chat):
    msg = """
Привет 🫡
Я бот для игры в blackjack 🃏.
Перед началом ознакомьтесь с <a href='https://telegra.ph/Pravila-igry-v-Blackjack-03-10'>правилами</a>.

 🤖 Список моих команд:
/start_game - 🆕 Создать новую игру
/my_statistics - 📊 Статистика Ваших игр
/help - ❔ Правила игры
    """
    await app.store.tg_api.send_message(message=Message(chat=chat, text=msg))
