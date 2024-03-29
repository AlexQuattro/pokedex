from flask import request
from flask_restful import Resource

from pokedex.errors.not_found import TypeNotFoundError
from pokedex.managers.types import get_types, get_pokemons_from_type, add_type, get_type_name


class Types(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'
        unused = request.args.get('unused', 'false') == 'true'
        query = request.args.get('query', None)

        types = get_types(search=query, unused=unused)

        result = []
        for type in types:
            type_result = type.get_small_data()

            if pokemons:
                type_result['pokemons'] = []
                pokemons_of_this_type = get_pokemons_from_type(type.id)
                for pokemon in pokemons_of_this_type:
                    pokemon_result = pokemon.get_small_data()
                    type_result['pokemons'].append(pokemon_result)

            result.append(type_result)
        return result

    def put(self):
        name = request.json['name']
        generation_name = request.json['generation']
        new_type = add_type(name, generation_name)
        return new_type.get_small_data()


class Type (Resource):
    def get (self, type_name):
        type = get_type_name(type_name)
        if type is None:
            raise TypeNotFoundError(type_name)

        return type.get_small_data()

