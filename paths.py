from enum import Enum


class Paths(Enum):
    Api = ('POST', '/api/')

    Lights = ('GET', '/lights/')
    LightGET = ('GET', '/lights/<id>')
    LightPUT = ('PUT', '/lights/<id>')
    LightDEL = ('DELETE', '/lights/<id>')

    Groups = ('GET', '/groups/')
    GroupGET = ('GET', '/groups/<id>')

    GroupState = ('PUT', '/groups/<id>/action/')
    LightState = ('PUT', '/lights/<id>/state/')

