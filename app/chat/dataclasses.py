from dataclasses import dataclass


@dataclass
class Chat:
    chat_id: int
    games_played: int
    game_is_active: bool
