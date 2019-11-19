from flask import request
from flask_restful import Resource

from pokedex.errors.not_found import PokemonNotFoundError
from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon, edit_pokemon_stats


class Pokemons(Resource):
    def get(self):
        query = request.args['query']
        type = request.args.get('type')
        ability = request.args.get('ability')
        limit = request.args.get('limit')


        pokemons_matching = search_pokemons(query, type, ability, limit)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]



        add_pokemon_search_history(request.remote_addr, query)

        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            raise PokemonNotFoundError(pokemon_name)

        return pokemon.get_small_data()

    def patch(self, pokemon_name, stat, value):
        new_stat = edit_pokemon_stats(name=pokemon_name, stat= stat, new_value = value)
        return new_stat

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
