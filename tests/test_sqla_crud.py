from persipy.repository import Repository

from sqlar.repository import sqla_crud


class MyEntity:
    def __init__(self, id_: int):
        self.id = id_


@sqla_crud(for_entity=MyEntity)
class MyRepository(Repository[MyEntity, int]):
    pass


def test_sqla_crud():
    my_repo = MyRepository()
    my_entity = my_repo.get(42)
    assert my_entity.id == 42
