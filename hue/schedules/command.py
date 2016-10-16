

class Command:
    address = None
    body = None
    method = None

    _parent = None
    _only = ['address', 'body', 'method']

    def __init__(self, obj, parent=None):
        self._parent = parent
        self._map(obj)

    def _map(self, obj):
        """
        Description:
            Maps passed in data to the object
        """
        for key in obj:
            setattr(self, key, obj[key])

    def object(self):
        """
        Description:
            Generates object required for running a command
        """
        return {
            'address': self.address,
            'body': self.body,
            'method': self.method
        }