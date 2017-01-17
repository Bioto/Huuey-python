

class State:
    """
    Description:
        Holds state information for lights

    Attrs:
        on: Is the light on or off
        bri: Current brightness of the light
        hue: Current hue of light
        sat: Current saturation of light
        xy: Current CIE color
        ct: Current Color Temp
        alert: Current alert type (ex.. "none", "select", "lselect")
        effect: Dynamic effect of light
        colormore: Current color mode (ex... HS, XY, CT)
        reachable: Can this light be reached by the bridge

        _only: List of values that can actually be set for the state
        _parent: Reference to main huuey object
        _updated_values: Array of values to be used for request
    """
    on = None
    bri = None
    hue = None
    sat = None
    xy = None
    ct = None
    alert = None
    effect = None
    colormode = None
    reachable = None

    _only = ['on', 'bri', 'hue', 'sat', 'xy', 'ct', 'alert', 'effect',
             'transitiontime', 'bri_inc', 'sat_inc', 'hue_inc', 'ct_inc',
             'xy_inc']

    _parent = None
    _updated_values = []

    def __init__(self, obj, parent):
        self._parent = parent

        for key in obj:
            setattr(self, key, obj[key])

    def update(self, obj):
        """
        Description:
            Updates values on this object

        Attr:
            Obj: Dictionary of values
        """
        for key in obj:
            if hasattr(self, key):
                setattr(self, key, obj[key])

                self._updated_values.append(key)

    def object(self):
        """
        Description:
            Returns dictionary full of variables on this object
        """
        class_variables = [
            attr for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith(
                    ('__', '_'))]
        obj = {}

        for key in class_variables:
            if len(self._updated_values) > 0:
                if key in self._updated_values:
                    obj[key] = getattr(self, key)
            else:
                if key in self._only:
                    obj[key] = getattr(self, key)

        self._updated_values = []

        return obj
