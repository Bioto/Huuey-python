from hue import State
from huuey import Paths


class Group:
    """
    Description:
        Holds data for a single Group from the hues API

    Attrs:
        name: Name of the group
        lights: Array holding light instances related to this group
        type: Type of group
        action(state): Holds instance of State()

        _controller: Reference to main huuey object
        _newname: Holds string for updating the name of the group
        _id: ID of light
    """
    name = None
    lights = []
    type = ""
    action = None

    _controller = None
    _newname = None
    _id = None

    def __init__(self, obj, lights, controller):
        self._controller = controller
        self._lights = lights

        self._map(obj)

    def _map(self, obj):
        """
        Description:
            Maps the passed in data to the current object
        """
        for key in obj:
            if key == 'action':
                self.action = State(obj[key], self)
            elif key == 'lights':
                for light_id in obj[key]:
                    self.lights.append(self._controller.lights[light_id])
            else:
                setattr(self, key, obj[key])

    def setstate(self, obj):
        """
        Description:
            Updates the state object to prepare for actual request
        """
        self.action.update(obj)
        return self

    def update(self):
        """
        Description:
            Sends request to endpoint then pulls updated data directly from the API
        """
        self._controller.request(Paths.GroupState, self.action.object(), additional={
            '<id>': self._id
        })
        self.grab()

    def grab(self):
        """
        Description:
            Pulls fresh data from the API
        """
        group = self._controller.request(Paths.GroupGET, additional={
            '<id>': self._id
        })

        self._map(group)
