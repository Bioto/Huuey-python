import json
from requests import Request, Session


class Requester:
    @staticmethod
    def verifyconnection(url="http://google.com"):
        return Requester.request(url, method='GET', decode=False)

    @staticmethod
    def request(url, method=None, data=None, decode=True):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        request = Request(method, url)

        if data:
            request.data = json.dumps(data)

        with Session() as session:
            prepped = session.prepare_request(request)

            try:
                response = session.send(prepped)
            except:
                return False

        if decode:
            return json.loads(response.text)
        else:
            return response
