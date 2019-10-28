from flask import request
from flask_restful import Resource

from pokedex.managers.species import get_species, get_specie, new_specie

class Species(Resource):
    def get(self):
        query = request.args.get('name', 'false') == 'true'
        species = get_species()

        result = []
        for specie in species:
            species_result = specie.get_small_data()

            if query:
                result.append(species_result['name'])
            else:
                result.append(species_result)


        return result


class Specie(Resource):
    def get(self):
        query = request.args['query']
        pokemon = get_specie(query)
        if pokemon is None:
            return {'msg': 'Not found'}, 404

        return pokemon.get_small_data()

    def put(self):
        name = request.json['name']
        new_spe = new_specie(name)

        return new_spe.get_small_data()