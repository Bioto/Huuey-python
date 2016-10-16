from enum import Enum


class Paths(Enum):
    Api = ('POST', '/api/')

    Lights = ('GET', '/lights/')
    LightGET = ('GET', '/lights/<id>')
    LightPUT = ('PUT', '/lights/<id>')
    LightDEL = ('DELETE', '/lights/<id>')

    Groups = ('GET', '/groups/')
    GroupGET = ('GET', '/groups/<id>')

    Schedules = ('GET', '/schedules/')
    SchedulesPOST = ('POST', '/schedules/')
    SchedulesDEL = ('DEL', '/schedules/<id>')

    GroupState = ('PUT', '/groups/<id>/action/')
    LightState = ('PUT', '/lights/<id>/state/')

