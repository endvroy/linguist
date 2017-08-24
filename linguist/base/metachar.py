from enum import Enum, unique


@unique
class MetaChar(Enum):
    epsilon = 0
    eof = 1


epsilon = MetaChar.epsilon
eof = MetaChar.eof
