from sqlalchemy import String
from typing import Optional

from persipy import CRUDRepository
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper

from sqlar.repository import sqla_crud


class Fixture:
    def __init__(self):
        class MyEntity:
            def __init__(self, id_: int, name: Optional[str]):
                self.id = id_
                self.name = name

        self._engine = create_engine('sqlite://')
        metadata = MetaData()
        my_entity_table = Table(
            'my_entities',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
        )
        mapper(MyEntity, my_entity_table)

        @sqla_crud
        class MyRepository(CRUDRepository[MyEntity, int]):
            pass

        metadata.create_all(bind=self._engine)
        self.repository = MyRepository(engine=self._engine)

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

    result = fixture.execute('SELECT id FROM my_entities;')
    assert list(result) == [(2,)]
    assert fixture.repository.find_by_id(1) is None


def test_delete_many():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')
    entity_1 = fixture.repository.find_by_id(1)
    entity_3 = fixture.repository.find_by_id(3)

    # Act
    fixture.repository.delete_many([entity_1, entity_3])

    result = fixture.execute('SELECT id FROM my_entities;')
    assert list(result) == [(2,)]
    assert fixture.repository.find_by_id(1) is None
    assert fixture.repository.find_by_id(3) is None


def test_delete_all():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')

    # Act
    fixture.repository.delete_all()

    count = fixture.execute('SELECT COUNT(*) FROM my_entities;').scalar()
    assert count == 0


def test_delete_by_id():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2);')

    # Act
    fixture.repository.delete_by_id(1)

    result = fixture.execute('SELECT id FROM my_entities;')
    assert list(result) == [(2,)]


def test_exists_by_id():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2);')

    # Act
    exists = fixture.repository.exists_by_id(2)

    assert exists is True


def test_not_exists_by_id():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2);')

    # Act
    exists = fixture.repository.exists_by_id(3)

    assert exists is False


def test_find_all():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')

    # Act
    entities = fixture.repository.find_all()

    ids = [entity.id for entity in entities]
    assert len(ids) == 3
    assert set(ids) == {1, 2, 3}


def test_find_all_by_id():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')

    # Act
    entities = fixture.repository.find_all_by_id([1, 4, 3])

    ids = [entity.id for entity in entities]
    assert len(ids) == 2
    assert set(ids) == {1, 3}


def test_find_by_id():
    fixture = Fixture()
    fixture.execute('INSERT INTO my_entities (id) VALUES (1), (2), (3);')

    # Act
    entity = fixture.repository.find_by_id(2)

    assert entity.id == 2


def test_save():
    fixture = Fixture()
    fixture.execute("INSERT INTO my_entities (id, name) VALUES (1, 'old'), (2, 'old'), (3, 'old');")
    entity = fixture.repository.find_by_id(2)
    entity.name = 'new'

    # Act
    entity = fixture.repository.save(entity)

    assert entity.name == 'new'
    entities = fixture.execute('SELECT id, name FROM my_entities;').fetchall()
    entities = [(id_, name) for id_, name in entities]
    assert len(entities) == 3
    assert set(entities) == {(1, 'old'), (2, 'new'), (3, 'old')}


def test_save_many():
    fixture = Fixture()
    fixture.execute("INSERT INTO my_entities (id, name) VALUES (1, 'old'), (2, 'old'), (3, 'old');")
    entities = fixture.repository.find_all_by_id([1, 3])
    for entity in entities:
        entity.name = 'new'

    # Act
    entities = fixture.repository.save_many(entities)

    entities = list(entities)
    assert len(entities) == 2
    assert all(entity.name == 'new' for entity in entities)
    entities = fixture.execute('SELECT id, name FROM my_entities;').fetchall()
    entities = [(id_, name) for id_, name in entities]
    assert len(entities) == 3
    assert set(entities) == {(1, 'new'), (2, 'old'), (3, 'new')}
