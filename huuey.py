
from requester import Requester
from paths import Paths


class Huuey:
    requester = None

    token = None
    address = None

    bridges = []

    verified = False

    class ExceptionNoToken(Exception):
        pass

    def __init__(self, token=None, address=None):
        self.requester = Requester()
        self.token = token
        self.address = address

        auth_set = self.token is None
        address_set = self.address is None

        if auth_set or address_set:
            self.discover()

    def discover(self):
        """ Grabs list of devices from meethue.com """
        if self.requester.verifyconnection():
            self.bridges = self.requester.request('www.meethue.com/api/nupnp', 'GET')

    def request(self, url=None, type=None, data=None):
        """ Builds and sends request

        Args:
            url: Root url
            type: Paths Enum
            data: Dict of data for request
            token: Bridge auth token

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
        url_set = url is None
        type_set = type is None
        token_set = self.token is None

        if url_set or type_set:
            return False

        if type is Paths.Api:
            url = "".join([url, type.value[1]])
        else:
            if token_set:
                raise self.ExceptionNoToken('Token missing from api call')

            url = "".join([url, "/api/", self.token, type.value[1]])

        return self.requester.request(url=url, type=type.value[0], data=data)

    def pair(self, id=None):
        if id is None:
            return False

        internal_ip = self.bridges[id]['internalipaddress']
        return self.request(internal_ip, Paths.Api, {
            "devicetype": "huuey"
        })
