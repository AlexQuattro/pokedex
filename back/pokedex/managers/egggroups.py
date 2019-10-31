import requests

from pokedex.models.pokemon import EggGroup, PokemonSpeciesEggGroups, PokemonSpecies, Pokemon, PokemonSpeciesVariety


def load_egg_group_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/egg-group/{name}')
    data = request.json()

    egg_group = EggGroup.get_or_none(name=data['name'])
    if egg_group is None:
        egg_group = EggGroup.create(name=data['name'])

    return egg_group


def load_egg_groups_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/egg-group/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for egg_group in data['results']:
            load_egg_group_from_api(egg_group['name'])
            i += 1

        print(f'{i} egg groups loaded.')

    return i


def get_egg_groups():
    egg_groups = EggGroup.select()
    return egg_groups


def get_egggroups_of_species(species):
    egggroups = PokemonSpeciesEggGroups.select(PokemonSpeciesEggGroups, EggGroup).join(EggGroup).where(
        PokemonSpeciesEggGroups.pokemon_species << species)

    pokemons_by_specie = {}
    for egggroup in egggroups:
        if egggroup.pokemon_species.id not in pokemons_by_specie.keys():
            pokemons_by_specie[egggroup.pokemon_species.id] = []
        pokemons_by_specie[egggroup.pokemon_species.id].append(egggroup.egg_group)

    return pokemons_by_specie


def get_species_from_egggroup(egg_id):
    pokemons = []
    pokemon_eggs = PokemonSpeciesEggGroups.select(PokemonSpeciesEggGroups, PokemonSpecies).join(PokemonSpecies).where(PokemonSpeciesEggGroups.egg_group == egg_id)

    for pokemon_egg in pokemon_eggs:
        pokemons.append(pokemon_egg.pokemon_species)

    return pokemons