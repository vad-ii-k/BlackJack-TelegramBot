from app.game.enums import CallbackData, Commands
from app.game.logic import (
    create_game,
    join_game,
    makes_turn,
    place_bet,
    send_msg_to_create_game,
    send_player_stats,
    send_rules,
    start_game,
)
from app.game.states import PlayerState
from app.store.tg_api.dataclassess import (
    AnswerCallbackQuery,
    CallbackQuery,
    MessageUpdate,
    MyChatMemberUpdate,
)
from app.web.app import app


async def handle_message(message: MessageUpdate):
    if not message.text:
        return
    command = message.text.removesuffix(f"@{app.config.bot.name}")
    match command:
        case Commands.START:
            await send_rules(message.chat)
        case Commands.START_GAME:
            await send_msg_to_create_game(message)
        case Commands.MY_STATISTICS:
            await send_player_stats(message.from_user, message.chat)
        case Commands.HELP:
            await send_rules(message.chat)


async def handle_my_chat_member(my_chat_member: MyChatMemberUpdate):
    await send_rules(my_chat_member.chat)


async def handle_callback_query(cb_query: CallbackQuery):
    match cb_query.data.split(":", maxsplit=1)[0]:
        case CallbackData.CREATE:
            cb_answer_text = await create_game(cb_query.message)
        case CallbackData.JOIN:
            cb_answer_text = await join_game(cb_query)
        case CallbackData.START:
            cb_answer_text = await start_game(cb_query)
        case CallbackData.BET:
            cb_answer_text = await place_bet(cb_query)
        case CallbackData.HIT:
            cb_answer_text = await makes_turn(
                cb_query, PlayerState.waiting_for_hand
            )
        case CallbackData.STAND:
            cb_answer_text = await makes_turn(
                cb_query, PlayerState.waiting_for_results
            )
        case _:
            cb_answer_text = "Действие не обработано"

    await app.store.tg_api.answer_callback_query(
        answer=AnswerCallbackQuery(
            id=cb_query.id,
            text=cb_answer_text,
        )
    )
