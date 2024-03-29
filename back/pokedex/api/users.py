from flask_restful import Resource

from pokedex.managers.users import sum_of_requests_of_user_agent, add_user_agent


class Users(Resource):
    def get(self):
        sum_requests = sum_of_requests_of_user_agent()

        add_user_agent()

        return sum_requests