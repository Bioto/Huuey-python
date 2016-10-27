from huuey.paths import Paths


class Scene:
    name = None
    lights = []
    owner = None
    recycle = None
    locked = None
    appdata = None
    picture = None
    lastupdated = None
    version = None

    _id = None
    _parent = None

    def __init__(self, obj, parent, _id):
        self._parent = parent
        self._id = _id

        self._map(obj)

    def get_id(self):
        return self._id

    def _map(self, obj):
        for key in obj:
            setattr(self, key, obj)

    @staticmethod
    def create(name, lights, controller, recycle=False):
        request = controller.request(Paths.SceneCREATE, data={
            'name': name,
            'lights': lights,
            'recycle': recycle
        })

        return request[0]['success']['id']

    def activate(self):
        return self._parent.request(Paths.SceneGroup, data={
            'scene': self._id
        })

    def delete(self):
        self._parent.request(Paths.SceneDEL, additional={
            'id': self._id
        })

        self._parent.remove_scene(self._id)
