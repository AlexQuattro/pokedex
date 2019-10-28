from peewee import *
from .database import db
from pokedex.managers.users import get_log


class Users(Model):
    id = PrimaryKeyField()
    url = CharField()
    method = CharField()

    class Meta:
        database = db
        schema = 'pokemon'

    def put_log(self):
        log = get_log()
        return log


with db:
    Users.create_table(fail_silently=True)