from enum import Enum


class GameState(str, Enum):
    started = "started"
    in_progress = "in_progress"
    finished = "finished"


class PlayerState(str, Enum):
    waiting_for_hand = "waiting_for_hand"
    makes_turn = "makes_turn"
    waiting_for_results = "waiting_for_results"
