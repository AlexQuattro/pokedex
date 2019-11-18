from pokedex.models.collections import User, Collection, PokemonCollection
from pokedex.models.pokemon import Pokemon


def create_user_or_collection(collection_name=None, pokemon_name=None, name=None):
    username = User.get_or_none(name=name)
    if username is None:
        user_created = User.create(name=name)
        return user_created.get_small_data()

    pokemon = Pokemon.get_or_none(name=pokemon_name)
    if pokemon_name is not None:
        data = pokemon.get_small_data()
        pokemon_created = PokemonCollection.create(id_pokemon=data['id'], name=data['name'], hp=data['stats']['hp'],
                                                   special_attack=data['stats']['special-attack'],
                                                   defense=data['stats']['defense'],
                                                   attack=data['stats']['attack'],
                                                   special_defense=data['stats']['special-defense'],
                                                   speed=data['stats']['speed'], sprite_back=data['sprite_back'],
                                                   sprite_front=data['sprite_front'])

        collection = Collection.get_or_none(collection_name=collection_name)
        if collection is None:
            result = Collection.create(collection_name=collection_name, user=username.id, pokemon=pokemon_created.id)
            return result.get_small_data()
        else:
            result = Collection.insert(collection_name=collection_name, user=username.id,
                                       pokemon=pokemon_created.id).execute()
            return {'pokemon_id': result}


def get_user(username=None):
    if username is not None:
        user = User.get_or_none(name=username)
        if user is not None:
            return True
        else:
            return False


def get_collection(collection_name=None):
    if collection_name is not None:
        collection = Collection.get_or_none(collection_name=collection_name)
        if collection is not None:
            return collection.get_small_data()
        else:
            return False


def get_pokemon(pokemon_name=None):
    if pokemon_name is not None:
        pokemon = PokemonCollection.get_or_none(name=pokemon_name)
        if pokemon is not None:
            return pokemon.get_small_data()
        else:
            return False


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


def fight(user_1,collection_user_1, user_2,collection_user_2):
    user_1 = Collection.select(Collection,User).join(User).where(User.name == user_1, Collection.collection_name == collection_user_1)
    user_2 = Collection.select(Collection,User).join(User).where(User.name == user_2, Collection.collection_name == collection_user_2)

    user_1_query = PokemonCollection.select(PokemonCollection).join(Collection).where(Collection.collection_name == collection_user_1)
    user_2_query = PokemonCollection.select(PokemonCollection).join(Collection).where(Collection.collection_name == collection_user_2)

    user_1_pokemons = [i.get_small_data() for i in user_1_query]
    user_2_pokemons = [i.get_small_data() for i in user_2_query]

    for pokemon_1 in user_1_pokemons:
        for pokemon_2 in user_2_pokemons:
            if pokemon_1['speed'] > pokemon_2['speed']:
                while float(pokemon_1['hp']) > 0 or float(pokemon_2['hp']) > 0:
                    new_hp_2 = float(pokemon_2['hp']) - max(1,(float(pokemon_1['attack']) - float(pokemon_2['defense'])))
                    new_hp_1 = float(pokemon_1['hp']) - max(1,(float(pokemon_2['attack']) - float(pokemon_1['defense'])))
                    return { 'pokemon_user_1' : new_hp_1,'pokemon_user_2': new_hp_2}