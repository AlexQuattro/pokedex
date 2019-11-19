class NotFoundError(Exception):
    def __init__(self, resource, resource_id):
        Exception.__init__(self)
        self.resource = resource
        self.resource_id = resource_id


class PokemonNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Pokemon", resource_id)


class TypeNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, 'Type', resource_id)

class Ability_Generation_NameNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, 'Ability_Generation_Name', resource_id)