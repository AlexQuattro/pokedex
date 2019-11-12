from flask import request
from flask_restful import Resource

from pokedex.managers.abilities import get_ability, get_verbose, get_generation_of_this_ability

class Abilities(Resource):

    def get(self):
        pokemons = request.args.get('verbose', 'false') == 'true'
        generation = request.args.get('generation')
        limit = request.args.get('limit')
        offset = request.args.get('offset')

        abilities = get_ability(offset=offset)

        result = []
        for ability in abilities:
            ability_result = ability.get_small_data()

            if pokemons:
                ability_result['effects'] = []
                verbose_of_this_ability = get_verbose(ability.id)
                for pokemon in verbose_of_this_ability:
                    pokemon_result = pokemon.effect
                    ability_result['effects'].append(pokemon_result)

            if generation:
                ability_result['generation'] = []
                data_of_this_generation = get_generation_of_this_ability(ability.id)
                for pokemon in data_of_this_generation:
                    pokemon_result = pokemon.name
                    ability_result['generation'].append(pokemon_result)

            result.append(ability_result)

            if limit is not None:
                result = result[:int(limit)]

        return result