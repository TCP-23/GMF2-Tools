from enum import Enum

# Enum for all supported games (BLOOD+ not yet supported)
class GameTarget_Enum(Enum):
    UNK = 1
    NMH1 = 2
    NMH2 = 3
    BLOOD = 4


class TargetGame:
    gameId = GameTarget_Enum.UNK
