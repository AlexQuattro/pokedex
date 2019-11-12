from peewee import *
from playhouse.shortcuts import model_to_dict


from .database import db


class CommonModel(Model):
    def get_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'analytics'


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()


class UserAgent(CommonModel):
    id = PrimaryKeyField()
    user_agent = CharField()


class Stats(CommonModel):
    id = PrimaryKeyField()
    moy = FloatField()


with db:
    SearchHistory.create_table(fail_silently=True)
    UserAgent.create_table(fail_silently=True)
    Stats.create_table(fail_silently=True)