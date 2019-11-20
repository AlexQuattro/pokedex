from flask import request
from flask_restful import Resource

from pokedex.managers.collections import create_collection, delete_user, get_user, get_collection, \
    get_pokemon, modify_pokemon, get_pokemons_by_collection, delete_collection, delete_pokemon, create_user, \
    add_pokemon, get_information_by_pokemon


class Collections(Resource):
    def get(self):
        user = request.args.get('user')
        collection = request.args.get('collection')
        pokemon = request.args.get('pokemon','false') == 'true'

        user_query = get_user(user)
        collection_query = get_collection(collection)

        result = []
        if user_query is not None:
            user = {'user': user_query.name}
            result.append(user)

            if collection_query is not None:
                collection_query = {'collection_name': collection_query['collection_name']}
                user['collection'] = []
                pokemons_by_collection = get_pokemons_by_collection(collection)
                collection_query['pokemon'] = [pokemon.name for pokemon in pokemons_by_collection]
                user['collection'].append(collection_query)

                if pokemon:
                    for pokemon in collection_query['pokemon']:
                        information_of_this_pokemon = get_information_by_pokemon(pokemon)
                        for information in information_of_this_pokemon:
                            pokemon_information = information.get_small_data()
                            collection_query['pokemon'].append(pokemon_information)

        return result

    def post(self):
        user = request.args.get('user')
        collection = request.args.get('collection')
        pokemon = request.args.get('pokemon')

        result = []
        if user is not None:
            result.append(create_user(name=user))
            if collection is not None:
                result.append(create_collection(collection_name=collection, name=user))
            if pokemon is not None:
                result.append(add_pokemon(collection=collection, pokemon_name=pokemon))
        return result

    def patch(self):
        pokemon_name = request.args['pokemon']
        stats = request.json

        for stat in stats.keys():
            modify_pokemon(pokemon_name, stat, stats[stat])

        edited_pokemon = get_pokemon(pokemon_name)

        return edited_pokemon

    def delete(self):
        user = request.args['user']
        collection = request.args.get('collection')
        pokemon = request.args.get('pokemon')

        if collection is not None and pokemon is not None:
            delete = delete_user(user)
            if collection is not None:
                delete = delete_collection(collection)
                if pokemon is not None:
                    delete = delete_pokemon(pokemon)
            return delete
