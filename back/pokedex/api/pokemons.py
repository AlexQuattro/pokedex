from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon, edit_pokemon_stats
from pokedex.managers.types import get_types

class Pokemons(Resource):
    def get(self):
        query = request.args['query']
        pokemons_matching = search_pokemons(query, type=None)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]

        add_pokemon_search_history(request.remote_addr, query)

        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['speed'], data['special-defense'], data['special-attack'], data['defense'], data['attack'], data['hp'])
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            return {'msg': 'Not found'}, 404

        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        return 'panic', 500

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result

    def patch(self, pokemon_name):
        data = request.json
        print(data)
        pokemon = get_pokemon_by_name(pokemon_name)
        edit_pokemon_stats(pokemon_name, data['stats'])
        return pokemon.get_small_data()

