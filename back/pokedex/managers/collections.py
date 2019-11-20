from pokedex.models.collections import User, Collection, PokemonCollection
from pokedex.models.pokemon import Pokemon
from pokedex.errors.not_found import PokemonNotFoundError, UserNotFoundError, CollectionNotFoundError


def create_user(name=None):
    username = User.get_or_none(name=name)

    if username is None:
        user_created = User.create(name=name)
        result = 'User created'
    else:
        result = 'User already exists'
    return result


def create_collection(name, collection_name=None):
    user = User.get_or_none(name=name)
    collection = Collection.get_or_none(collection_name=collection_name)

    if collection is None:
        collection_created = Collection.create(collection_name=collection_name, user_id=user.id)
        result = 'Collection created'
    else:
        result = 'Collection already exists'
    return result


def add_pokemon(collection, pokemon_name=None):
    collection_name = Collection.get_or_none(collection_name=collection)
    pokemon = Pokemon.get_or_none(name=pokemon_name)

    if pokemon is not None:
        data = pokemon.get_small_data()

        pokemon_created = PokemonCollection.create(id_pokemon=data['id'], collection_id=collection_name.id,
                                                   name=data['name'], hp=data['stats']['hp'],
                                                   special_attack=data['stats']['special-attack'],
                                                   defense=data['stats']['defense'],
                                                   attack=data['stats']['attack'],
                                                   special_defense=data['stats']['special-defense'],
                                                   speed=data['stats']['speed'])

        return pokemon_created.get_small_data()
    else:
        raise PokemonNotFoundError(pokemon_name)


def get_user(username=None):
    if username is not None:
        user = User.get_or_none(name=username)
        if user is None:
            raise UserNotFoundError(username)
        else:
            return user


def get_collection(collection_name=None):
    if collection_name is not None:
        collection = Collection.get_or_none(collection_name=collection_name)
        if collection is None:
            raise CollectionNotFoundError(collection_name)
        else:
            return collection.get_small_data()


def get_pokemon(pokemon_name=None):
    if pokemon_name is not None:
        pokemon = PokemonCollection.get_or_none(name=pokemon_name)
        if pokemon is None:
            raise PokemonNotFoundError(pokemon_name)
        else:
            return pokemon.get_small_data()


def modify_pokemon(name, stat, new_value):
    update = {stat: new_value}
    pokemon = PokemonCollection.update(**update).where(PokemonCollection.name == name).execute()
    return pokemon


def delete_user(username):
    user = User.get_or_none(name=username)
    user.delete_instance(recursive=True)
    return True


def delete_collection(collection_name):
    collection = Collection.get_or_none(collection_name=collection_name)
    collection.delete_instance(recursive=True)
    return True


def delete_pokemon(pokemon_name):
    pokemon = PokemonCollection.get_or_none(name=pokemon_name)
    pokemon.delete_instance(recursive=True)
    return True


def get_pokemons_by_collection(collection_name):
    pokemons = PokemonCollection.select().join(Collection).where(Collection.collection_name == collection_name)
    return pokemons


def get_information_by_pokemon(pokemon_name):
    pokemon = Pokemon.select().where(Pokemon.name == pokemon_name)
    return pokemon
