from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from typing import Generic
from typing import MutableMapping
from typing import Optional
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')


class CustomRepository(Generic[T, K]):
    def __init__(self):
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._identity_map: Optional[MutableMapping[K, T]] = None
        self._sessions: Optional[MutableMapping[T, Session]] = None
