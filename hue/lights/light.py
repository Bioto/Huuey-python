from hue.state import State
from huuey import Paths


class Light:
    """
    Description:
        Holds data for a single Light from the hues API

    Attrs:
        state: Holds instance of State()
        type: Type of group
        name: Name of the group
        modelid: Type of Light
        swversion: Software Version
        uniqueid: Machine id for light

        _id: ID of light
        _controller: Reference to main huuey object
        _newname: Holds string for updating the name of the group
    """
    state = None
    type = None
    name = None
    modelid = None
    swversion = None
    uniqueid = None

    _id = None
    _controller = None
    _newname = None

    def __init__(self, obj, controller):
        self._controller = controller
        self._map(obj)

    def _map(self, obj):
        """
        Description:
            Maps the passed in data to the current object
        """
        for key in obj:
            if key == "state":
                self.state = State(obj[key], self)
            else:
                setattr(self, key, obj[key])

    def delete(self):
        """
        Description:
            Deletes the Light from the bridge
        """
        return self._controller.request(Paths.LightDEL, additional={
            '<id>': self._id
        })

    def setstate(self, obj):
        """
        Description:
            Updates the state object to prepare for actual request
        """
        if 'rename' in obj:
            self._newname = obj['rename']
            del obj['rename']

        self.state.update(obj)
        return self

    def update(self):
        """
        Description:
            Sends request to endpoint then pulls updated data directly from the API

            If _newname is set it will send the request to update the name first
            then trigger main request
        """
        if self._newname:
            self._controller.request(Paths.LightPUT, {
                'name': self._newname
            }, additional={
                '<id>': self._id
            })

            self._newname = None

        self._controller.request(Paths.LightState, self.state.object(), additional={
            '<id>': self._id
        })
        self.grab()

    def grab(self):
        """
        Description:
            Pulls fresh data from the API
        """
        light = self._controller.request(Paths.LightGET, additional={
            '<id>': self._id
        })

        self._map(light)
