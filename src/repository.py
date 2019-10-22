from abc import abstractmethod
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')


class MyEntity:
    def __init__(self, id_: int):
        self.id = id_


def fetch_from_database(id_: int) -> MyEntity:
    return MyEntity(id_)


class Repository(Generic[T, K]):
    @abstractmethod
    def get(self, id_: K) -> T:
        pass


def sqla_repository(repository_class):
    class RepositoryImpl:
        def __init__(self):
            self._identity_map = {}  # TODO: WeakRef?

        def get(self, id_):
            instance = self._identity_map.get(id_)
            if instance is None:
                self._identity_map[id_] = instance = fetch_from_database(id_)
            return instance

    # TODO: inspect repository_class interface to generate more methods

    return RepositoryImpl


@sqla_repository
class MyRepository(Repository[MyEntity, int]):
    pass


my_repo = MyRepository()
my_entity = my_repo.get(42)
print('ID =', my_entity.id)
