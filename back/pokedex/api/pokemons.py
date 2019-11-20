from flask import request
from flask_restful import Resource

from pokedex.errors.not_found import PokemonNotFoundError
from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon, modify_stat
from pokedex.managers.users import add_user_agent
from pokedex.managers.forms import get_forms_from_pokemon
from pokedex.managers.abilities import get_abilities_from_pokemon


class Pokemons(Resource):
    def get(self):
        query = request.args['query']
        type = request.args.get('type')
        form = request.args.get('form', 'false') == 'true'
        limit = request.args.get('limit', None)
        ability_query = request.args.get('ability')
        abilities = request.args.get('abilities', 'false') == 'true'

        add_pokemon_search_history(request.remote_addr, query)
        add_user_agent()

        pokemons_matching = search_pokemons(query, type=type, limit=limit, ability_query=ability_query)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]

        if form:
            for pokemon in pokemons:
                pokemon['forms'] = []

                forms_of_this_pokemon = get_forms_from_pokemon(pokemon['id'])

                for form in forms_of_this_pokemon:
                    pokemon['forms'].append(form.name)

        if abilities:
            for pokemon in pokemons:
                pokemon['abilities'] = []

                abilities_of_this_pokemon = get_abilities_from_pokemon(pokemon['id'])

                for ability in abilities_of_this_pokemon:
                    pokemon['abilities'].append(ability.ability.name)

        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['speed'], data['special-defense'], data['special-attack'], data['defense'], data['attack'], data['hp'])
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        form = request.args.get('form', 'false') == 'true'

        if pokemon is None:
            raise PokemonNotFoundError(pokemon_name)

        pokemon = pokemon.get_small_data()

        if form:
            pokemon['forms'] = []

            forms_of_this_pokemon = get_forms_from_pokemon(pokemon['id'])

            for form in forms_of_this_pokemon:
                pokemon['forms'].append(form.name)

        return pokemon

    def patch(self, pokemon_name):
        stats = request.json

        for stat in stats.keys():
            modify_stat(pokemon_name, stat, stats[stat])

        pokemon_edited = get_pokemon_by_name(pokemon_name)

        return pokemon_edited.get_small_data()

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result