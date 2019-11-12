from pokedex.models.pokemon import Generation, Ability, Type
from peewee import fn


def get_generations(query=None):
    generations = Generation.select()

    if query is not None:
        generations = Generation.select().where(Generation.name.contains(query))
    return generations


def get_number_of_abilities_by_generation():
    query = Generation.select(Generation.name, fn.Count(Generation.name).alias('count')).join(Ability).group_by(
        Generation.name)
    result = [{'generation': i.name, 'count': i.count} for i in query]

    return result


def get_number_of_types_by_generation():
    query = Generation.select(Generation.name, fn.Count(Generation.name).alias('count')).join(Type).group_by(
        Generation.name)
    result = [{'generation': i.name, 'count': i.count} for i in query]

    return result


def add_generation(generation_name):
    generation = Generation.get_or_none(name=generation_name)
    if generation is None:
        generation = Generation.create(name=generation_name)
    else:
        generation.save()

    return generation


def get_generation(name):
    generation = Generation.get_or_none(name=name)
    return generation
