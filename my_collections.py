from my_exceptions import TriggerSyntaxException
import collections


class NameTracker(collections.MutableMapping):
    """
    A dictionary that raises a TriggerSyntaxException if an attempt is made to add a key that already exists.

    Keys must be deleted before replacing them.
    """
    def __init__(self, init_dict=None):
        # type: (dict) -> None
        self.instances = {}
        if init_dict:
            for key in init_dict:
                self[key] = init_dict[key]

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

    def __iter__(self):
        for key in self.instances:
            yield key

    def __len__(self):
        return len(self.instances)

    def __str__(self):
        return 'NameTracker'+str(self.instances)

    def __repr__(self):
        return str(self)


class ValidatedDict(collections.MutableMapping):
    """
    A dictionary which has a set of valid keys. If an attempt is made to add a key that is not in the set of valid keys,
    a TriggerSyntaxException is raised.
    """
    def __init__(self, valid_keys, map=None):
        self._map = {}
        self._valid_keys = valid_keys

        if map:
            for key in map:
                self[key] = map[key]

    def __getitem__(self, key):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+key+"'is not a valid argument.")
        return self._map[key]

    def __setitem__(self, key, value):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+key+"'is not a valid argument.")
        self._map[key] = value

    def __delitem__(self, key):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+key+"'is not a valid argument.")
        del self._map[key]

    def __iter__(self):
        for key in self._map:
            yield key

    def __len__(self):
        return len(self._map)

    def __str__(self):
        return 'ValidatedDict'+str(self._map)

    def __repr__(self):
        return str(self)