from enum import Enum, auto


class State(Enum):
    NONE = auto()
    ASK_CITY = auto()
    ASK_DETAILS = auto()
    FINISHED = auto()


class UserDataSlots:
    __slots__ = ['user_id', 'state', 'city']
    def __init__(self, user_id=0, state=State.NONE, city=None):
        self.user_id =user_id
        self.state = state
        self.city = city


from dataclasses import dataclass

@dataclass(slots=True)
class UserDataDC:
    user_id: int = 0
    state: State = State.NONE
    city: str = ''


if __name__ == '__main__':
    import sys
    users = [UserDataSlots(1, State.NONE, 'kaluga'), UserDataDC(2, State.NONE, 'kaluga')]
    for user in users:
        print('----------')
        print(user)
        user.city = 'Kaluga'
        print(user.city)
        try:
            user.a = 1
        except Exception as ex:
            print(ex.args)
        finally:
            print(dir(user))
        print(sys.getsizeof(user))
        print('----------')