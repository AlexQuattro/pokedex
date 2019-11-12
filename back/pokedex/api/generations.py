from flask import request
from flask_restful import Resource

from pokedex.managers.generations import get_generations, get_number_of_abilities_by_generation, \
    get_number_of_types_by_generation, add_generation, get_generation


class Generations(Resource):
    def get(self):
        filter = request.args.get('filter')
        number_abilities = request.args.get('number of abilities', 'false') == 'true'
        number_types = request.args.get('number of types by generation', 'false') == 'true'

        generations = get_generations(filter)
        result = [generation.get_small_data() for generation in generations]

        if number_abilities is not None:
            result = get_number_of_abilities_by_generation()

        if number_types is not None:
            result = get_number_of_types_by_generation()

        return result

    def put(self):
        data = request.json
        variety = add_generation(data['name'])
        return variety.get_small_data()


class Generation(Resource):
    def get(self, generation_name):
        return get_generation(generation_name).get_small_data()
