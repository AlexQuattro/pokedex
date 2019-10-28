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
from flask import request
from flask_restful import Resource

from pokedex.managers.species import get_species, get_pokemons_of_species, get_specie, add_variety


class Species(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'

        species = get_species()
        results = [specie.get_small_data() for specie in species]
        if pokemons:
            pokemons_by_species = get_pokemons_of_species(species)
            for specie in results:
                specie['pokemons'] = [p.name for p in pokemons_by_species[specie['id']]]

        return results

    def put(self):
        data = request.json
        variety = add_variety(data['specie'], data['pokemon'], data.get('is_default', False))
        return variety.get_small_data()


class Specie(Resource):
    def get(self, specie_id):
        specie = get_specie(specie_id)
        results = specie.get_small_data()

        pokemons_by_species = get_pokemons_of_species([specie])
        results['pokemons'] = [p.get_small_data() for p in pokemons_by_species[specie.id]]

        return results
