from flask_restful import Resource

from pokedex.managers.scrapping import get_pokemons


class Scrapping(Resource):
    def get(self):
        pokemons = get_pokemons()
        result = [pokemon.get_small_data() for pokemon in pokemons]

        return result
