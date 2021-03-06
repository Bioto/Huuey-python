
from requester import Requester
from paths import Paths
from .hue import Light, Group, Schedule, Scene

from cli import CommandLine


class ExceptionNoToken(Exception):
    """
    Description:
        Exception that's thrown if a token is not set when making an api call
    """
    pass


class ExceptionAuthNotSet(Exception):
    """
    Description:
        Exception that's thrown if auth variables are not set
    """
    pass


class Huuey:
    token = None
    address = None

    bridges = []
    lights = {}
    groups = {}
    schedules = {}
    scenes = {}

    verified = False

    def cli(self):
        print('Starting command line...')
        cmd = CommandLine()
        cmd.huuey = self
        cmd.cmdloop()

    def __init__(self, token=None, address=None):
        self.token = token
        self.address = address

        auth_set = self.token is None
        address_set = self.address is None

        if auth_set or address_set:
            self.discover()

    def issetup(self):
        """
        Description:
            Checks if token and address is set and returns true/false
        """
        return self.token and self.address

    def discover(self):
        """ Grabs list of devices from meethue.com """
        if Requester.verifyconnection():
            self.bridges = Requester.request('www.meethue.com/api/nupnp',
                                             'GET')

    def request(self, type=None, data=None, additional=None):
        """ Builds and sends request

        Args:
            type: Paths Enum
            data: Dict of data for request
            additional: Dict of data which takes the key and maps it to the keys value if set in string

        Returns:
            After sending the request it returns one of the following:
                json decoded object: Response from api
                false: Something went wrong with the call

            Json Decode Object Example:
                [
                    {
                        "error":{
                            "type":101,
                            "address":"/",
                            "description":
                            "link button not pressed"
                        }
                    }
                ]
        Raises:
            ExceptionNoToken:
                Token isn't being set on Huuey()
        """
        address_set = self.address is not None
        type_set = type is not None
        token_set = self.token is not None

        if not address_set or not type_set:
            return False

        if type is Paths.Api:
            url = "".join([self.address, type.value[1]])
        else:
            if not token_set:
                raise ExceptionNoToken('Token missing from api call')

            url = "".join([self.address, "/api/", self.token, type.value[1]])

        if additional:
            for key in additional:
                url = url.replace(key, additional[key])

        request = Requester.request(url=url, method=type.value[0], data=data)
        
        return request

    def pair(self, local_id=None):
        """
        Description:
            Pair class to bridge

        Args:
            local_id: local index for bridge
        """
        if local_id is None:
            return False

        self.address = self.bridges[local_id]['internalipaddress']
        return self.request(Paths.Api, {
            "devicetype": "huuey"
        })

    def set_auth(self, local_id=None, token=None):
        """
        Description:
            Verifies that local_id and token are set and sets up auth object

        Args:
            local_id: Index for pulling found bridge
            token: Token used to authorize requests to the bridge

        Raises:
            ExceptionAuthNotSet:
                Bridge index or token not set when calling set_auth
        """
        local_id_set = local_id is not None
        token_set = token is not None

        if not local_id_set and not token_set:
            error = 'Bridge ID or Token not set: [Bridge ID:{}] [Token:{}]'.format(local_id, token)
            raise ExceptionAuthNotSet(error)

        self.address = self.bridges[local_id]['internalipaddress']
        self.token = token

        self.update()

    def create_scene(self, name, lights, recycle):
        scene_id = Scene.create(name=name, lights=lights, controller=self, recycle=recycle)
        return self.update()._scan_scenes(scene_id)

    def create_group(self, name, lights):
        group_id = Group.create(name=name, lights=lights, controller=self)
        return self.update()._scan_groups(group_id)

    def remove_scene(self, _id):
        del self.scenes[_id]

    def update(self):
        """
        Description:
            Triggers pulling latest data from the bridge
        """
        self._grab_lights()
        self._grab_groups()
        self._grab_schedules()
        self._grab_scenes()

        return self

    def _grab_lights(self):
        """
            Description:
                Grab all lights from bridge and stores locally on self
        """
        lights = self.request(Paths.Lights)

        for index in lights:
            lights[index]['_id'] = index
            self.lights[index] = Light(obj=lights[index], controller=self)

    def _scan_groups(self, _id):
        for group in self.groups:
            if self.groups[group].get_id() == _id:
                return self.groups[group]

    def _grab_groups(self):
        """
            Description:
                Grab all groups from bridge and stores locally on self
        """
        groups = self.request(Paths.Groups)

        for index in groups:
            groups[index]['_id'] = index
            self.groups[index] = Group(obj=groups[index], controller=self)

    def _grab_schedules(self):
        """
            Description:
                Grab all schedules from bridge and stores locally on self
        """
        schedules = self.request(Paths.Schedules)

        for index, schedule in enumerate(schedules):
            schedules[schedule]['_id'] = index
            self.schedules[schedule] = Schedule(parent=self, obj=schedules[schedule])

    def _scan_scenes(self, _id):
        for scene in self.scenes:
            if self.scenes[scene].get_id() == _id:
                return self.scenes[scene]

    def _grab_scenes(self):
        scenes = self.request(Paths.Scenes)

        for index, scene in enumerate(scenes):
            self.scenes[index] = Scene(obj=scenes[scene], parent=self, _id=scene)
