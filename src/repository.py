from typing import Dict
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')


class Repository(Generic[T, K]):
    def __init__(self):
        self._identity_map: Dict[K, T] = {}

    def get(self, id_: K) -> T:
        return self._identity_map[id_]


class MyEntity:
    def __init__(self, id_: int):
        self.id = id_


class MyRepository(Repository[MyEntity, int]):
    def __init__(self):
        super().__init__()
        self._identity_map[42] = MyEntity(42)


my_repo = MyRepository()
my_entity = my_repo.get(42)
print('ID =', my_entity.id)
