import random

from app.game.keyboards import GameKeyboard
from app.game.models import GameModel
from app.game.states import PlayerState
from app.store.tg_api.dataclassess import Message
from app.web.app import app

SUITS = ["♠️", "♣️", "♥️", "♦️"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

EMOJI_BY_STATE = {
    PlayerState.waiting_for_hand: " —",
    PlayerState.makes_turn: "🤔",
    PlayerState.waiting_for_results: "😴",
    PlayerState.won: "🤑",
    PlayerState.draw: "🤗",
    PlayerState.lost: "😡",
}


def players_roster(
    game: GameModel, with_cards: bool = False, with_score: bool = False
) -> str:
    roster = "<u>Список игроков</u>: \n"
    for player in game.players:
        roster += EMOJI_BY_STATE[player.state]
        roster += f" {player.user.name}"
        roster += f": {player.hand}" * with_cards
        roster += f" ({final_score(player.score)})" * with_score
        roster += "\n" + "ㅤ\n" * with_cards
    return roster


def scores_as_int(score: str) -> tuple[int, int]:
    score_1, score_2 = tuple(map(int, score.split("/")))
    return score_1, score_2


def calc_new_score(old_score: str, new_card_rank: str) -> str:
    score_1, score_2 = scores_as_int(old_score)

    if new_card_rank == "A":
        score_1 += 1
        score_2 += 11 if score_2 < 11 else 1
    else:
        cost = int(new_card_rank) if new_card_rank.isdigit() else 10
        score_1 += cost
        score_2 += cost

    return f"{score_1}/{score_2}"


def final_score(scores: str) -> int:
    scores = scores_as_int(scores)
    return max(scores) if max(scores) <= 21 else min(scores)


def new_hand_and_score(old_hand: str, old_score: str) -> tuple[str, str]:
    rank, card = random.choice(RANKS), random.choice(SUITS)
    new_hand = f"{old_hand}{' • ' * (old_hand != '')}{rank}{card}"
    # new_hand example: 3♥️ • K♥️ • 5♣️
    new_score = calc_new_score(old_score, rank)
    return new_hand, new_score


async def deal_cards(game: GameModel):
    for player in game.players:
        hand, score = player.hand, player.score
        if hand == "":
            hand, score = new_hand_and_score(hand, score)
        if player.state is None or player.state == PlayerState.waiting_for_hand:
            hand, score = new_hand_and_score(hand, score)

            await app.store.game.update_player(
                player,
                state=PlayerState.makes_turn,
                hand=hand,
                score=score,
            )
    game = await app.store.game.get_active_game(game.chat_id)
    await auto_change_player_states(game)


async def auto_change_player_states(game: GameModel):
    for player in game.players:
        if final_score(player.score) > 21:
            await app.store.game.update_player(player, PlayerState.lost)
        elif final_score(player.score) == 21:
            await app.store.game.update_player(player, PlayerState.won)


def dealer_hand_and_final_score() -> tuple[str, int]:
    dealer_hand, dealer_scores = new_hand_and_score("", "0/0")
    while final_score(dealer_scores) < 17:
        dealer_hand, dealer_scores = new_hand_and_score(
            dealer_hand, dealer_scores
        )
    return dealer_hand, final_score(dealer_scores)


async def calc_game_results(game: GameModel, dealer_score: int):
    for player in game.players:
        if player.state == PlayerState.waiting_for_results:
            player_score = final_score(player.score)
            if player_score > 21 or player_score < dealer_score <= 21:
                new_state = PlayerState.lost
            elif player_score != dealer_score:
                new_state = PlayerState.won
            else:
                new_state = PlayerState.draw
            player = await app.store.game.update_player(player, new_state)
        await app.store.game.update_player_statistics(
            player,
            player.state == PlayerState.won,
            player.state == PlayerState.lost,
        )


async def finish_game(game: GameModel, message: Message):
    dealer_hand, dealer_score = dealer_hand_and_final_score()
    await calc_game_results(game, dealer_score)
    game = await app.store.game.get_active_game(message.chat.id)

    message.text = (
        f"Игра окончена!\nㅤ\n"
        + players_roster(game, True, True)
        + f"🤖 Дилер: {dealer_hand} ({dealer_score})"
    )
    message.reply_markup.inline_keyboard = GameKeyboard.EMPTY
    await app.store.tg_api.edit_message(message)

    await app.store.game.finish_game(game)
