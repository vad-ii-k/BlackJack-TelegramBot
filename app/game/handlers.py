from app.game.keyboards import GameKeyboard
from app.game.logic import (
    create_game,
    join_game,
    makes_turn,
    send_player_stats,
    send_rules,
    start_game,
)
from app.game.states import PlayerState
from app.store.tg_api.dataclassess import (
    AnswerCallbackQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
    MessageUpdate,
    MyChatMemberUpdate,
)
from app.web.app import app


async def handle_message(message: MessageUpdate):
    if not message.text:
        return
    command = message.text.removesuffix(f"@{app.config.bot.name}")
    match command:
        case "/start_game":
            await app.store.tg_api.send_message(
                message=Message(
                    chat=message.chat,
                    text="Сыграем?",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=GameKeyboard.CREATE_GAME
                    ),
                )
            )
        case "/my_statistics":
            await send_player_stats(message.from_user, message.chat)
        case "/help":
            await send_rules(message.chat)


async def handle_my_chat_member(my_chat_member: MyChatMemberUpdate):
    await send_rules(my_chat_member.chat)


async def handle_callback_query(cb_query: CallbackQuery):
    match cb_query.data:
        case "create":
            cb_answer_text = await create_game(cb_query.message)
        case "join":
            cb_answer_text = await join_game(cb_query)
        case "start":
            cb_answer_text = await start_game(cb_query.message)
        case "hit":
            cb_answer_text = await makes_turn(
                cb_query, PlayerState.waiting_for_hand
            )
        case "stand":
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
