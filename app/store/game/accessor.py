from typing import Union

from sqlalchemy import Select, and_, select, update
from sqlalchemy.engine import ChunkedIteratorResult

from app.base.base_accessor import BaseAccessor
from app.game.models import (
    ChatModel,
    GameModel,
    PlayerModel,
    PlayerStatisticsModel,
    UserModel,
)
from app.game.states import GameState, PlayerState

Model = Union[
    ChatModel, GameModel, PlayerModel, PlayerStatisticsModel, UserModel
]


class GameAccessor(BaseAccessor):
    async def _select_first(self, query: Select) -> Model | None:
        async with self.app.database.session.begin() as session:
            result: ChunkedIteratorResult = await session.execute(query)
            return result.scalars().first()

    async def _add_object(self, obj: Model) -> Model:
        async with self.app.database.session.begin() as session:
            session.add(obj)
        return obj

    async def _get_chat(self, chat_id: int) -> ChatModel | None:
        query = select(ChatModel).where(ChatModel.chat_id == chat_id)
        return await self._select_first(query)

    async def _create_chat(self, chat_id: int) -> ChatModel:
        return await self._add_object(ChatModel(chat_id=chat_id))

    async def _get_user(self, tg_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.tg_id == tg_id)
        return await self._select_first(query)

    async def _create_user(self, tg_id: int, name: str) -> UserModel:
        return await self._add_object(UserModel(tg_id=tg_id, name=name))

    async def get_player(self, tg_id: int) -> PlayerModel | None:
        query = select(PlayerModel).where(PlayerModel.tg_id == tg_id)
        return await self._select_first(query)

    async def create_player(self, tg_id: int, user_name: str) -> PlayerModel:
        user = await self._get_user(tg_id)
        if user is None:
            await self._create_user(tg_id, user_name)

        player = await self._add_object(PlayerModel(tg_id=tg_id))
        await self._add_object(PlayerStatisticsModel(tg_id=tg_id))
        return player

    async def add_player_to_game(
        self, player: PlayerModel, game_id: int
    ) -> PlayerModel:
        query = (
            update(PlayerModel)
            .values(game_id=game_id, state=PlayerState.waiting_for_hand)
            .where(PlayerModel.tg_id == player.tg_id)
            .returning(PlayerModel)
        )
        return await self._select_first(query)

    async def update_player(
        self,
        player: PlayerModel,
        state: PlayerState | None = None,
        hand: str | None = None,
        score: str | None = None,
        bet: int | None = None,
        balance: int | None = None,
    ) -> PlayerModel:
        query = (
            update(PlayerModel)
            .values(
                hand=hand or player.hand,
                score=score or player.score,
                bet=bet or player.bet,
                balance=balance or player.balance,
                state=state,
            )
            .where(PlayerModel.tg_id == player.tg_id)
            .returning(PlayerModel)
        )
        return await self._select_first(query)

    async def get_active_game(self, chat_id: int) -> GameModel | None:
        query = select(GameModel).where(
            and_(
                GameModel.chat_id == chat_id,
                GameModel.state != GameState.finished,
            )
        )
        return await self._select_first(query)

    async def create_game(self, chat_id: int, message_id: int) -> GameModel:
        chat = await self._get_chat(chat_id)
        if chat is None:
            await self._create_chat(chat_id)

        return await self._add_object(
            GameModel(chat_id=chat_id, message_id=message_id)
        )

    async def update_game(self, game: GameModel, state: GameState) -> GameModel:
        query = (
            update(GameModel)
            .values(state=state)
            .where(GameModel.id == game.id)
            .returning(GameModel)
        )
        return await self._select_first(query)

    async def finish_game(self, game: GameModel):
        query = (
            update(PlayerModel)
            .values(game_id=None, hand="", score="0/0", state=None, bet=None)
            .where(PlayerModel.game_id == game.id)
            .returning(PlayerModel)
        )
        await self._select_first(query)
        await self.update_game(game, state=GameState.finished)

    async def get_player_statistics(
        self, tg_id: int
    ) -> PlayerStatisticsModel | None:
        query = select(PlayerStatisticsModel).where(
            PlayerStatisticsModel.tg_id == tg_id
        )
        return await self._select_first(query)

    async def update_player_statistics(
        self,
        player: PlayerModel,
        won: bool,
        lost: bool,
    ) -> PlayerStatisticsModel:
        player_stats = await self.get_player_statistics(player.tg_id)
        query = (
            update(PlayerStatisticsModel)
            .values(
                games_played=player_stats.games_played + 1,
                games_won=player_stats.games_won + won,
                games_lost=player_stats.games_lost + lost,
            )
            .where(PlayerStatisticsModel.tg_id == player.tg_id)
            .returning(PlayerStatisticsModel)
        )
        return await self._select_first(query)
