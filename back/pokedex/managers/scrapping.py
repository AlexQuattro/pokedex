import requests
from lxml import html
from tqdm import tqdm

from pokedex.models.scrapping import Pokemon


def load_pokemons_from_wikipedia():
    wikipedia_request = requests.get('https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon')
    xpath = '/ html / body / div[3] / div[3] / div[4] / div / table[3]'

    tree = html.fromstring(wikipedia_request.content)
    pokemons_tables = tree.xpath(xpath)

    pokemons_table = pokemons_tables[0]
    pokemons_table_rows = pokemons_table.findall('.//tr')

    pokemons = {}
    symbols = {}

    for row in pokemons_table_rows[2:]:
        pokemon_id = None

        i = 0

        for column in row.findall('td'):

            try:
                if i % 2 == 0:
                    content = column.text_content()
                    if 'No additional' not in content:
                        pokemon_id = int(content)
                        symbols[pokemon_id] = None

                if '#9FCADF' in column.attrib['style']:
                    pokemon_symbol = 'Starter'
                elif '#ccdfdc' in column.attrib['style']:
                    pokemon_symbol = 'Fossil'
                elif '#F7D9D3' in column.attrib['style']:
                    pokemon_symbol = 'Baby'
                elif '#E89483' in column.attrib['style']:
                    pokemon_symbol = 'Legendary'
                elif '#DCD677' in column.attrib['style']:
                    pokemon_symbol = 'Mythical'
                elif '#B7A3C3' in column.attrib['style']:
                    pokemon_symbol = 'Ultra Beast'
                else:
                    pokemon_symbol = ''

                symbols[pokemon_id] = pokemon_symbol

            except KeyError:
                pass

            pokemons_table_img = pokemons_table.findall('.//img')
            for img in pokemons_table_img:
                image = img.attrib['src']  # url
                # print(img.get('alt')) # nom

            if i % 2 == 0:
                content = column.text_content()
                if 'No additional' not in content:
                    pokemon_id = int(content)
                    pokemons[pokemon_id] = None
                else:
                    i += 1

            else:
                symbols_to_strip = ['\n', '※', '♭', '~', '♯']
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
        Pokemon.create(id=pokemon_id, name=pokemon_name, symbol='', generation='')

    for symbol in symbols.keys():
        if symbols[symbol] is not None:
            Pokemon.update(symbol=symbols[symbol]).where(Pokemon.id == symbol).execute()

    query = Pokemon.select(Pokemon.id)
    pokemons = [pokemon.get_small_data() for pokemon in query]
    for pokemon in pokemons:
        if pokemon['id'] < 152:
            Pokemon.update(generation='generation I').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 252:
            Pokemon.update(generation='generation II').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 387:
            Pokemon.update(generation='generation III').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 494:
            Pokemon.update(generation='generation VI').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 650:
            Pokemon.update(generation='generation V').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 722:
            Pokemon.update(generation='generation VI').where(Pokemon.id == pokemon['id']).execute()
        elif pokemon['id'] < 810:
            Pokemon.update(generation='generation VII').where(Pokemon.id == pokemon['id']).execute()
        else:
            Pokemon.update(generation='generation VIII').where(Pokemon.id == pokemon['id']).execute()


def get_pokemons():
    pokemons = Pokemon.select().order_by(Pokemon.id)
    result = [pokemon for pokemon in pokemons]
    return result
