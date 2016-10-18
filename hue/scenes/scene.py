

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

    def __init__(self, obj, parent, id):
        self._parent = parent
        self._id = id

        self._map(obj)

    def _map(self, obj):
        for key in obj:
            setattr(self, key, obj)
