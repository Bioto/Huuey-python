from enum import Enum


class Paths(Enum):
    Api = ('POST', '/api/')

    Lights = ('GET', '/lights/')
    LightGET = ('GET', '/lights/<id>')
    LightPUT = ('PUT', '/lights/<id>')
    LightDEL = ('DELETE', '/lights/<id>')

    Groups = ('GET', '/groups/')
    GroupGET = ('GET', '/groups/<id>/')
    GroupPUT = ('PUT', '/groups/<id>/')
    GroupCREATE = ('POST', '/groups/')
    GroupDELETE = ('DEL', '/groups/<id>/')

    Schedules = ('GET', '/schedules/')
    SchedulesPOST = ('POST', '/schedules/')
    SchedulesDEL = ('DEL', '/schedules/<id>')

    Scenes = ('GET', '/scenes/')
    SceneGroup = ('PUT', '/groups/0/action')
    SceneCREATE = ('POST', '/scenes/')
    SceneDEL = ('DEL', '/scenes/<id>')

    GroupState = ('PUT', '/groups/<id>/action/')
    LightState = ('PUT', '/lights/<id>/state/')

