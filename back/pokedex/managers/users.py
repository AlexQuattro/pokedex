from pokedex.api.__init__ import register_api

from pokedex.models.users import Users


def get_log():
    log = register_api()
    data = {'method': log['method'], 'url': log['url']}
    user_log = Users.create(**data)
    return user_log