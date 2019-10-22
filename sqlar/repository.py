def sqla_crud(for_entity):
    def wrapper(repository_cls):
        class RepositoryImpl:
            def __init__(self):
                self._identity_map = {}  # TODO: WeakRef?

            def get(self, id_):
                instance = self._identity_map.get(id_)
                if instance is None:
                    self._identity_map[id_] = instance = for_entity(id_)
                return instance

        # TODO: inspect repository_cls interface to generate more methods

        return RepositoryImpl

    return wrapper
