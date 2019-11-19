import requests

from pokedex.models.pokemon import Generation


def get_generations():
    species = Generation.select()
    return species


def get_pokemons_from_generations(filter):
    pass


def get_generation(filter):
    pass