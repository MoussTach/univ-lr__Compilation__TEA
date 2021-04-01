from enum import Enum


class CategoryDesc(Enum):
    COMMENTARY = "C"
    META = "M"
    INPUT = "V"
    OUTPUT = "O"
    NB_STATES = "E"
    INIT = "I"
    FINAL = "F"
    TRANSITIONS = "T"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
