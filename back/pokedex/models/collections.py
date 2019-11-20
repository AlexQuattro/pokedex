from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'collections'


class User(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


class Collection(CommonModel):
    id = PrimaryKeyField()
    collection_name = CharField()
    user = ForeignKeyField(User)


class PokemonCollection(CommonModel):
    id = PrimaryKeyField()
    collection_id = ForeignKeyField(Collection)
    id_pokemon = CharField()
    name = CharField()
    hp = CharField()
    special_attack = CharField()
    defense = CharField()
    attack = CharField()
    special_defense = CharField()
    speed = CharField()


with db:
    User.create_table(fail_silently=True)
    Collection.create_table(fail_silently=True)
    PokemonCollection.create_table(fail_silently=True)
