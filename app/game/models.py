from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, relationship

from app.game.states import GameState, PlayerState
from app.store.database.sqlalchemy_base import db


class UserModel(db):
    __tablename__ = "users"

    tg_id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(Text, nullable=False, unique=False)

    player: Mapped["PlayerModel"] = relationship(back_populates="user")


class PlayerModel(db):
    __tablename__ = "players"

    tg_id = Column(
        BigInteger,
        ForeignKey("users.tg_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)
    hand = Column(Text, default="", nullable=False, unique=False)
    state = Column(
        Enum(PlayerState),
        nullable=True,
        unique=False,
    )
    score = Column(Text, default="0/0", nullable=False, unique=False)

    user: Mapped[UserModel] = relationship(
        back_populates="player", lazy="joined"
    )
    game: Mapped["GameModel"] = relationship(
        back_populates="players", order_by="PlayerModel.tg_id"
    )


class PlayerStatisticsModel(db):
    __tablename__ = "players_statistics"

    tg_id = Column(
        BigInteger,
        ForeignKey("players.tg_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    games_played = Column(Integer, default=0, unique=False)
    games_won = Column(Integer, default=0, unique=False)
    games_lost = Column(Integer, default=0, unique=False)


class ChatModel(db):
    __tablename__ = "chats"

    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)


class GameModel(db):
    __tablename__ = "games"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"), nullable=False)
    state = Column(
        Enum(GameState), server_default=GameState.created, unique=False
    )

    players: Mapped[list[PlayerModel]] = relationship(
        back_populates="game", lazy="selectin"
    )
