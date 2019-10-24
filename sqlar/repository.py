import sqlalchemy
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedClassError
from typing import Iterable
from typing import Optional
from typing import TypeVar

from persipy import CRUDRepository

T = TypeVar('T')
K = TypeVar('K')


def sqla_crud(repository_cls):
    if not issubclass(repository_cls, CRUDRepository):
        raise TypeError('Repository must be inherited from CRUDRepository before annotating with sqla_crud')

    entity_cls = repository_cls.__entity_cls__

    try:
        mapper = class_mapper(entity_cls)
    except UnmappedClassError:
        raise TypeError('Invalid SQLAlchemy entity class given')

    if len(mapper.tables) > 1:
        raise TypeError('sqla_crud does not support entities mapped to multiple tables')

    entity_table = mapper.tables[0]

    class RepositoryImpl(repository_cls):
        """
        SQLAlchemy implementation for CRUDRepository (persipy)
        This repository implementation is not thread-safe.
        """
        class RepositoryException(Exception):
            pass

        def count(self) -> int:
            return self._bind.execute(
                sqlalchemy.select([func.count()]).select_from(entity_table),
            ).scalar()

        def delete(self, entity: T):
            try:
                session = self._sessions[entity]
            except KeyError:
                raise self.RepositoryException('Entity must be fetched with repository before being deleted')
            pk = inspect(entity).identity
            if len(pk) == 1:
                pk = pk[0]
            del self._identity_map[pk]
            session.delete(entity)
            session.flush()
            del self._sessions[entity]

        def delete_many(self, entities: Iterable[T]):
            for entity in entities:
                self.delete(entity)

        def delete_all(self):
            self._bind.execute(
                sqlalchemy.delete(entity_table),
            )
            self._identity_map = {}
            self._sessions = {}

        def delete_by_id(self, id_: K):
            pass

        def exists_by_id(self, id_: K) -> bool:
            pass

        def find_all(self) -> Iterable[T]:
            pass

        def find_all_by_id(self, ids: Iterable[K]) -> Iterable[T]:
            pass

        def find_by_id(self, id_: K) -> Optional[T]:
            if id_ in self._identity_map:
                return self._identity_map[id_]

            session = self._session_factory()
            instance = session.query(entity_cls).get(id_)
            if instance is None:
                return None

            self._identity_map[id_] = instance
            self._sessions[instance] = session
            return instance

        def save(self, entity: T) -> T:
            pass
            # if entity not in self._sessions:
            #     raise self.RepositoryException(f'Entity must be fetched with repository before saving: {entity}')
            # self._sessions[entity].flush()
            # return entity

        def save_many(self, entities: Iterable[T]) -> Iterable[T]:
            pass

        def __init__(self, bind: Engine):
            self._bind = bind
            self._session_factory = sessionmaker(bind=self._bind)
            self._identity_map = {}
            self._sessions = {}

    # TODO: inspect repository_cls interface to generate more methods

    return RepositoryImpl
