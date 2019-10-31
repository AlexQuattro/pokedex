from flask import request
from flask_restful import Resource

from pokedex.managers.egggroups import get_egg_groups, get_species_from_egggroup
from pokedex.managers.species import get_pokemons_of_species, get_species


class Egggroups(Resource):
    def get(self):
        egg = request.args.get("egggroup", 'false') == 'true'
        pokemons = request.args.get("pokemons", 'false') == 'true'

        egggroups = get_egg_groups()

        results = []
        for egggroup in egggroups:
            egg_result = egggroup.get_small_data()

            if egg:
                egg_result['species'] = []
                species_by_egggroup = get_species_from_egggroup(egggroup.id)
                for specie in species_by_egggroup:
                    specie_result = {'id': specie.id, 'name': specie.name}
                    egg_result['species'].append(specie_result)
            results.append(egg_result)

            species = get_species()
            pokemon_results = [specie.get_small_data() for specie in species]

            if pokemons:
                pokemons_by_species = get_pokemons_of_species(species)
                for specie in pokemon_results:
                    for p in pokemons_by_species[specie['id']]:
                        results.append(p.name)

        return results
