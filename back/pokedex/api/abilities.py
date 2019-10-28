from flask import request
from flask_restful import Resource

from pokedex.managers.abilities import get_ability, get_verbose

class Abilities(Resource):

    def get(self):
        pokemons = request.args.get('verbose', 'false') == 'true'
        abilities = get_ability()

        result = []
        for ability in abilities:
            ability_result = ability.get_small_data()

            if pokemons:
                ability_result['verbose'] = []
                verbose_of_this_ability = get_verbose(ability.id)
                for pokemon in verbose_of_this_ability:
                    pokemon_result = {'verbose': pokemon.effect}
                    ability_result['verbose'].append(pokemon_result)

            result.append(ability_result)
        return result