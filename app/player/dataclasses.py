from dataclasses import dataclass

from app.game.models import PlayerModel, PlayerStatisticsModel


@dataclass
class Player:
    tg_id: int
    balance: int
    games_played: int
    games_won: int
    games_lost: int

    @classmethod
    def from_db(cls, player: PlayerModel, player_stats: PlayerStatisticsModel):
        return cls(
            tg_id=player.tg_id,
            balance=player.balance,
            games_played=player_stats.games_played,
            games_won=player_stats.games_won,
            games_lost=player_stats.games_lost,
        )
