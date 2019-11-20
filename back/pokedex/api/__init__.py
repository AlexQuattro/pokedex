from flask import Blueprint
from flask_restful import Api

from pokedex.errors import NotFoundError
from pokedex.models.database import db

from .pokemons import Pokemon, Pokemons
from .species import Species, Specie
from .abilities import Abilities
from .types import Types
from .egg_groups import EggGroups
from .users import Users
from .stats import Stats
from .collections import Collections
from .generations import Generations, Generation
from .scrapping import Scrapping

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_api(app):
    @api_bp.before_request
    def before_request():
        db.connect(reuse_if_open=True)
        pass

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()

    @api_bp.errorhandler(NotFoundError)
    def if_not_found(error):
        response = {"error": f"{error.resource} {error.resource_id} not found"}
        return response, 404

    api.add_resource(Pokemons, '/pokemons')
    api.add_resource(Pokemon, '/pokemon/<pokemon_name>')
    api.add_resource(Types, '/types')
    api.add_resource(Species, '/species')
    api.add_resource(Specie, '/specie/<specie_id>')
    api.add_resource(EggGroups, '/egggroups')
    api.add_resource(Abilities, '/abilities')
    api.add_resource(Users, "/users")
    api.add_resource(Stats, "/stats")
    api.add_resource(Collections, '/collections')
    api.add_resource(Generations, '/generations')
    api.add_resource(Generation, '/generation/<generation_name>')
    api.add_resource(Scrapping, "/scrapping")

    app.register_blueprint(api_bp, url_prefix="/api/v1")
