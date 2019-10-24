from persipy import CRUDRepository
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper

from sqlar.repository import sqla_crud


class MyEntity:
    def __init__(self, id_: int):
        self.id = id_


class Fixture:
    def __init__(self):
        self._engine = create_engine('sqlite://')
        metadata = MetaData()
        my_entity_table = Table('my_entities', metadata, Column('id', Integer, primary_key=True))
        mapper(MyEntity, my_entity_table)

        @sqla_crud
        class MyRepository(CRUDRepository[MyEntity, int]):
            pass

        metadata.create_all(bind=self._engine)
        self.repository = MyRepository(bind=self._engine)

    def execute(self, sql):
        return self._engine.execute(sql)


def test_count():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')

    # Act
    count = fixture.repository.count()

    assert count == 3


def test_delete():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2);')
    entity = fixture.repository.find_by_id(1)

    # Act
    fixture.repository.delete(entity)

    result = fixture.execute('SELECT * FROM my_entities;')
    assert result == [(2,)]
    assert fixture.repository.find_by_id(1) is None
