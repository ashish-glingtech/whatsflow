from flask import Blueprint
from flask_restful import Api

from .webhook import IncomingMessageWebhook

blueprint = Blueprint(__name__)
api = Api(blueprint)

api.add_resource(IncomingMessageWebhook, "/webhook")
