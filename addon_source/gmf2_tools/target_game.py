from enum import Enum


class GameTarget_Enum(Enum):
    UNK = 1
    NMH1 = 2
    NMH2 = 3
    BLOOD = 4


class TargetGame:
    gameId = GameTarget_Enum.UNK
