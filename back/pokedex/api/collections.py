from flask import request
from flask_restful import Resource

from pokedex.managers.collections import create_user_or_collection, delete_user, get_user, get_collection, \
    get_pokemon, modify_pokemon, get_pokemons_by_collection, delete_collection, delete_pokemon, fight


class Collections(Resource):
    def get(self):
        user = request.args.get('user')
        collection = request.args.get('collection')
        pokemon = request.args.get('pokemon')

        user_query = get_user(user)
        collection_query = get_collection(collection)
        pokemon_query = get_pokemon(pokemon)

        if user_query is not None:
            return user_query
        if collection_query is not None:
            pokemons_by_collection = get_pokemons_by_collection(collection)
            collection_query['pokemon'] = [pokemon.name for pokemon in pokemons_by_collection]
            return collection_query
        if pokemon_query is not None:
            return pokemon_query
        else:
            return False

    def post(self):
        user = request.args.get('user')
        collection = request.args.get('collection')
        pokemon = request.args.get('pokemon', None)

        collection_create = create_user_or_collection(collection_name=collection, pokemon_name=pokemon, name=user)

        if collection_create is not None:
            return collection_create

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


    def put(self):
        user_1 = request.args['user_1']
        user_2 = request.args['user_2']
        collection_user_1 = request.args['collection_user_1']
        collection_user_2 = request.args['collection_user_2']

        result = fight(user_1=user_1,collection_user_1=collection_user_1,user_2=user_2,collection_user_2=collection_user_2)

        return result
