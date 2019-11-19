import requests
from lxml import html, etree
from tqdm import tqdm
import math

from bs4 import BeautifulSoup

from pokedex.models.scrapping import Pokemon


def load_pokemons_from_wikipedia():
    wikipedia_request = requests.get('https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon ')
    xpath = '/ html / body / div[3] / div[3] / div[4] / div / table[3]'

    tree = html.fromstring(wikipedia_request.content)
    pokemons_tables = tree.xpath(xpath)

    pokemons_table = pokemons_tables[0]
    pokemons_table_rows = pokemons_table.findall('.//tr')

    header =[]
    first_row = pokemons_table_rows[0]

    for cell in first_row.findall('th'):
        content = cell.text_content()
        header.append(content)


    pokemons = {}

    for row in pokemons_table_rows[2:]:
        pokemon_id = None

        i = 0
        for column in row.findall('td'):
            if i % 2 == 0:
                content = column.text_content()
                if 'No additional' not in content:
                    pokemon_id = int(content)
                    pokemons[pokemon_id] = None
                    value = header[math.floor(i/2)]
                else:
                    i += 1
            else:
                symbols_to_strip = ['\n', '※', '♭']
                pokemon_name = column.text_content()
                for symbol in symbols_to_strip:
                    pokemon_name = pokemon_name.strip(symbol)

                if pokemon_id is not None:
                    pokemons[pokemon_id] = pokemon_name
                    pokemon_id = None

            i += 1

    Pokemon.delete().execute()
    for pokemon_id in tqdm(pokemons.keys()):
        pokemon_name = pokemons[pokemon_id]
        pokemon_generation = value


        Pokemon.create(id=pokemon_id, name=pokemon_name, generation = pokemon_generation )
