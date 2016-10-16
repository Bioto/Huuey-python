
from requester import Requester
from paths import Paths
from hue import Light, Group


class Huuey:
    requester = None

    token = None
    address = None

    bridges = []
    lights = {}
    groups = {}

    verified = False

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

    def __init__(self, token=None, address=None):
        self.requester = Requester()
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
        if self.token or self.address:
            return True
        return False

    def discover(self):
        """ Grabs list of devices from meethue.com """
        if self.requester.verifyconnection():
            self.bridges = self.requester.request('www.meethue.com/api/nupnp', 'GET')

    def request(self, type=None, data=None, additional=None):
        """ Builds and sends request

        Args:
            type: Paths Enum
            data: Dict of data for request

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
                raise self.ExceptionNoToken('Token missing from api call')

            url = "".join([self.address, "/api/", self.token, type.value[1]])

        if additional:
            for key in additional:
                url = url.replace(key, additional[key])

        return self.requester.request(url=url, type=type.value[0], data=data)

    def pair(self, local_id=None):
        """
        Description:
            Pair class to bridge

        Args:
            local_id: local index for bridge
        """
        if id is None:
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
            raise self.ExceptionAuthNotSet(error)

        self.address = self.bridges[local_id]['internalipaddress']
        self.token = token

        self._grab_lights()
        self._grab_rooms()

    def _grab_lights(self):
        """
            Description:
                Grab all lights from bridge and stores locally on self
        """
        lights = self.request(Paths.Lights)

        for index in lights:
            lights[index]['_id'] = index
            self.lights[index] = Light(lights[index], self)

    def _grab_rooms(self):
        """
            Description:
                Grab all groups from bridge and stores locally on self
        """
        groups = self.request(Paths.Groups)

        for index in groups:
            groups[index]['_id'] = index
            self.groups[index] = Group(groups[index], self.lights, self)