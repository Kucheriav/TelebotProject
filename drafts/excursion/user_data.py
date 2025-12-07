from enum import Enum, auto
from dataclasses import dataclass


class State(Enum):
    NONE = auto()
    ASK_CITY = auto()
    ASK_DETAILS = auto()
    FINISHED = auto()

@dataclass(slots=True)
class UserData:
    user_id: int = 0
    state: State = State.NONE
    city: str = ''
    category: str = ''

if __name__ == '__main__':
    u_d = UserData()
    print(u_d)