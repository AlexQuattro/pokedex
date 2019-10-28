from pokedex.api.__init__ import register_api

from pokedex.models.users import Users


def get_log():
    log = register_api()
    Users.create({'method':log['method'],'url':log['url']})
    print('hello')