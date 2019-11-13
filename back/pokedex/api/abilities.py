from flask import request
from flask_restful import Resource

from pokedex.managers.abilities import get_abilities, get_ability_generation_name

class Abilities (Resource):
    def get(self):
        abilities = get_abilities()

        result = []
        for ability in abilities:
            result.append(ability.get_small_data())
        return result


class Ability (Resource):
    def get(self, ability_generation_name):
        ability = get_ability_generation_name(ability_generation_name)

        result = []
        if ability is None:
            return {'msg': 'Not found'}, 404
        for ab in ability:
            result.append(ab.get_small_data())

        return result
