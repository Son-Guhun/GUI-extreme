from my_exceptions import TriggerSyntaxException
import collections
import warnings


class NameTracker(collections.MutableMapping):
    """
    A dictionary that raises a TriggerSyntaxException if an attempt is made to add a key that already exists.

    Keys must be deleted before replacing them.
    """
    def __init__(self, init_dict=None, internal_type=None):
        # type: (collections.MutableMapping, type) -> None
        if not internal_type:
            self.instances = {}
        else:
            self.instances = internal_type()
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

    The valid keys container does not
    """

    # # noinspection PyClassHasNoInit
    # class __UninitializedValue:
    #     def __len__(self):
    #         return 0
    #
    # _UNINITIALIZED_VALUE = __UninitializedValue()
    UNINITIALIZED_VALUE = None

    def __init__(self, valid_keys, map_=None):
        self._map = {}
        self._valid_keys = valid_keys

        if map_:
            for key in map_:
                self[key] = map_[key]

    # region Implementation comment:
    # ------------
    # Returning None for keys that are valid but are not in _map
    # Vs.
    # Raising KeyError for valid keys that aren't in _map
    # ------------
    # Raising a KeyError would make ValidatedDict behave like a built-in dict. However, the second implementation was
    # chosen because it's more convenient to use in code and makes ValidatedDict behave as if it were an object with
    # defined members.
    # endregion
    def __getitem__(self, key):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+str(key)+"'is not a valid argument.")
        try:
            return self._map[key]
        except KeyError:
            return self.UNINITIALIZED_VALUE

    def __setitem__(self, key, value):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+str(key)+"'is not a valid argument.")
        self._map[key] = value

    def __delitem__(self, key):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+str(key)+"'is not a valid argument.")
        try:
            del self._map[key]
        except KeyError:
            warnings.warn('Deleted an uninitialized key '+str(key)+' in '+str(self), RuntimeWarning)

    def __iter__(self):
        for key in self._map:
            yield key

    def __len__(self):
        return len(self._map)

    def __str__(self):
        return 'ValidatedDict'+str(self._map)

    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        if key not in self._valid_keys:
            raise TriggerSyntaxException("'"+str(key)+"'is not a valid argument.")
        return key in self._map


class BlockParser(collections.Mapping):

    def __getitem__(self, k):
        # type: (str) -> list[list]
        return self._map[k]

    def __iter__(self):
        for key in self._map:
            yield key

    def __len__(self):
        len(self._map)

    def __init__(self):
        self._map = collections.OrderedDict()
        self._category = ''
        self._index = 0

    def set_category(self, name):
        raise NotImplementedError

    def new_category(self, name):
        if name in self._map:
            raise TriggerSyntaxException('Category ' + name + ' already exists!')

        self._map[name] = []
        self._category = name

    def new_block(self):
        self._map[self._category].append([])

    def add_line(self, line):
        try:
            self._map[self._category][-1].append(line)
        except IndexError:
            raise TriggerSyntaxException('Block member found outside block!')
