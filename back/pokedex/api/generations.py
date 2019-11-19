from flask import request
from flask_restful import Resource

from pokedex.managers.generations import get_generations, get_pokemons_from_generations, get_generation


class Generations(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'

        generations = get_generations()

        result = []
        for generation in generations:
            generation_result = generation.get_small_data()

            if pokemons:
                generation_result['pokemons'] = []
                pokemons_of_this_generation = get_pokemons_from_generations(generation.id)
                for pokemon in pokemons_of_this_generation:
                    pokemon_result = {'id': pokemon.id, 'name': pokemon.name}
                    generation_result['pokemons'].append(pokemon_result)

            result.append(generation_result)
        return result


class Generation (Resource):
    def get(self, generation_name):
        generation = get_generation(generation_name)
        results = generation.get_small_data()

        pokemons_by_generations = get_pokemons_from_generations([generation])
        results['pokemons'] = [p.get_small_data() for p in pokemons_by_generations[specie.id]]

        return results

