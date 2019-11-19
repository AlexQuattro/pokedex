from flask import request
from peewee import fn
from pokedex.models.analytics import UserAgent


def add_user_agent():
    get_ua = request.headers.get('User-Agent')
    add_ua = UserAgent.create(user_agent=get_ua)
    return add_ua


def sum_of_requests_of_user_agent():
    query = UserAgent.select(UserAgent.user_agent, fn.Count(UserAgent.user_agent).alias('count')).group_by(
        UserAgent.user_agent)
    result = [{'user_agent': i.user_agent, 'count': i.count} for i in query]

    return result