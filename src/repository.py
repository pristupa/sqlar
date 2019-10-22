from typing import TypeVar

from persipy.repository import Repository

T = TypeVar('T')
K = TypeVar('K')


class MyEntity:
    def __init__(self, id_: int):
        self.id = id_


def fetch_from_database(id_: int) -> MyEntity:
    return MyEntity(id_)


def sqla_crud(repository_class):
    class SQLAlchemyCRUDRepository:
        def __init__(self):
            self._identity_map = {}  # TODO: WeakRef?

        def get(self, id_):
            instance = self._identity_map.get(id_)
            if instance is None:
                self._identity_map[id_] = instance = fetch_from_database(id_)
            return instance

    # TODO: inspect repository_class interface to generate more methods

    return SQLAlchemyCRUDRepository


@sqla_crud
class MyRepository(Repository[MyEntity, int]):
    pass


my_repo = MyRepository()
my_entity = my_repo.get(42)
print('ID =', my_entity.id)
