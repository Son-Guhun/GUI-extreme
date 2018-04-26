from my_exceptions import TriggerSyntaxException


class NameTracker:
    """
    A dictionary that does raises a TriggerSyntaxException if an attempt is made to add a key that already exists.

    Keys must be deleted before replacing them.
    """
    def __init__(self):
        self.instances = {}

    def __getitem__(self, item):
        return self.instances[item]

    def __setitem__(self, key, value):
        if key in self.instances:
            raise TriggerSyntaxException(key + ": this symbol already exists!")
        else:
            self.instances[key] = value

    def __delitem__(self, key):
        if key in self.instances:
            del self.instances[key]
        else:
            raise TriggerSyntaxException(key + ": this symbol does not exist!")