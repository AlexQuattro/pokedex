from flask import request
from flask_restful import Resource

from pokedex.managers.generations import get_generations, get_number_of_abilities_by_generation, \
    get_number_of_types_by_generation, add_generation, get_generation


class Generations(Resource):
    def get(self):
        filter = request.args.get('filter')
        number_abilities = request.args.get('number_abilities', 'false') == 'true'
        number_types = request.args.get('number_types', 'false') == 'true'

        generations = get_generations(filter)
        result = [generation.get_small_data() for generation in generations]

        for number in result:
            if number_abilities:
                number['number_abilities'] = []
                number_of_this_ability = get_number_of_abilities_by_generation(number.id)
                for number in number_of_this_ability:
                    pokemon_result = {'generation':number.name,'count':number.count}
                    number['number_abilities'].append(pokemon_result)
            result.append(number)

        if number_types:
            result = get_number_of_types_by_generation()

        return result

    def put(self):
        data = request.json
        variety = add_generation(data['name'])
        return variety.get_small_data()


class Generation(Resource):
    def get(self, generation_name):
        return get_generation(generation_name).get_small_data()
