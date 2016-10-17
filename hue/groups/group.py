from hue import State
from hue.lights import Light
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
        _id: ID of light
    """
    name = None
    lights = {}
    type = ""
    action = None

    _controller = None
    _id = None

    _only_update = ['name', 'lights']

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
                    self.lights[light_id] = self._controller.lights[light_id]
            else:
                setattr(self, key, obj[key])

    def add_light(self, light):
        """
        Description:
            Adds passed in light (int or object) to group

        Attrs:
            light: (int or instance) adds light in specific ways depending on type
        """
        if type(light) is type(Light):
            self.lights[light.getid()] = light
        else:
            light = self._lights[str(light)]
            self.lights[light.getid()] = light

    def remove_light(self, light):
        """
        Description:
            Removes passed in light (int or object) to group

        Attrs:
            light: (int or instance) removes light in specific ways depending on type
        """
        if type(light) is type(Light):
            del self.lights[str(light.getid())]
        else:
            del self.lights[str(light)]

    def update(self):
        """
        Description:
            Sends request to update group to the bridge
        """
        request = self._controller.request(Paths.GroupPUT, data=self.object_update(), additional={
            '<id>': self._id
        })
        return request

    def object_update(self):
        """
        Description:
            Generates object used for updating name/lights on the group
        """
        obj = {
            'name': self.name,
            'lights': []
        }

        for light in self.lights:
            light_id = self.lights[light].getid()

            if light_id not in obj['lights']:
                obj['lights'].append(light_id)

        return obj

    def setstate(self, obj):
        """
        Description:
            Updates the state object to prepare for actual request
        """
        self.action.update(obj)
        return self

    def update_data(self):
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
