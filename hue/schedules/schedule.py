from command import Command
from huuey import Paths


class Schedule:
    name = None
    description = None
    command = None
    localtime = None
    status = True
    autodelete = False

    _parent = None
    _only = ['name', 'description', 'localtime', 'status', 'autodelete']
    _only_create = ["name", "description", "command", "localtime"]

    _id = None

    def __init__(self, parent, obj=None, **kwargs):
        self._parent = parent

        if obj:
            self._map(obj)
        else:
            self._map(kwargs)

    def _map(self, obj):
        """
        Description:
            Maps the passed in data to the current object
        """
        for key in obj:
            if key == "command":
                self.state = Command(obj[key])
            else:
                setattr(self, key, obj[key])

    def create_command(self, address, body, method):
        """
        Description:
            Creates new command instance for this schedule instance

        Attrs:
            address: Url to hit when schedule is called
            body: Data used to trigger specific updates
            method: What method should this command use
        """
        self.command = Command(obj={
            'address': address,
            'body': body,
            'method': method
        }, parent=self)

    def object(self):
        """
        Description:
            Creates object for updating schedule
        """
        obj = {}

        for key in self._only:
            obj[key] = getattr(self, key)

        obj['command'] = self.command.object()

        return obj

    def object_create(self):
        """
        Description:
            Creates object with specific fields required for creating a new schedule
        """
        obj = {}

        for key in self._only_create:
            obj[key] = getattr(self, key)

        obj['command'] = self.command.object()

        return obj

    def create(self):
        """
        Description:
            Triggers actual request to bridge
        """
        request = self._parent.request(type=Paths.SchedulesPOST, data=self.object_create())
        self._parent.update()
        return request

    def delete(self):
        """
        Description:
            Deletes schedule from bridge
        """
        request = self._parent.request(type=Paths.SchedulesDEL, additional={
            '<id>': self._id
        })
        self._parent.update()
        return request
