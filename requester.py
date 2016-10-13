import json
from requests import Request, Session


class Requester:
    session = None

    def __init__(self):
        self.session = Session()

    def verifyconnection(self, url="http://google.com"):
        return self.request(url, type='GET', decode=False)

    def request(self, url, type=None, data=None, decode=True):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        request = Request(type, url)

        if data:
            request.data = json.dumps(data)

        prepped = self.session.prepare_request(request)

        try:
            response = self.session.send(prepped)
        except:
            return False

        if decode:
            return json.loads(response.text)
        else:
            return response
