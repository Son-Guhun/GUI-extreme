from typing import Dict
import abc

from utilities import get_line_key
from my_collections import NameTracker
from my_exceptions import TriggerSyntaxException


class TriggerEditorObject(object):
    _instances = NameTracker()
    _class_sets = {}  # type: Dict[class, set]

    """
    An abstract class that represents an object which can be referenced by other objects within TriggerData.txt.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def params(self):
        """
        Yields the parameters declared after the equals sign in the object's declaration. Params don't necessarily
        have the string type. If you need strings, use (str(x) for x in .params()).

        :rtype: str(x) for every value x yielded by this generator must return the correct string in the final .txt file
        """
        yield None

    def __init__(self, **kwargs):
        super(TriggerEditorObject, self).__init__()

        self._name = kwargs['name']
        self._instances[self._name] = self
        self._class_sets[type(self)].add(self)

    def __del__(self):
        self.remove()

    def remove(self):
        del self._instances[self._name]
        self._class_sets[type(self)].remove(self)

    @property
    def name(self):
        # type: () -> str
        return self._name

    @name.setter
    def name(self, new_name):
        # type: (str) -> None
        self._instances[new_name] = self
        self.__del__()
        self._name = new_name

    def __str__(self):
        return self._name

    @classmethod
    def get_class_instances(cls):
        return cls._class_sets[cls]

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            for subsubclass in subclass.get_subclasses():
                yield subsubclass
            yield subclass

    @classmethod
    def get_object_from_name(cls, name):
        # type: (str) -> TriggerEditorObject
        try:
            return cls._instances[name]
        except KeyError:
            raise TriggerSyntaxException('Symbol ' + name + ' is not defined.')

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        """
        Parses a symbol declaration block, passed as a list of strings, where each element is a line.

        Example:
        [
        'EnumDestructablesInCircleBJMultiple=1,real,location',
        '_EnumDestructablesInCircleBJMultiple_Defaults=256,GetRectCenter',
        '_EnumDestructablesInCircleBJMultiple_Category=TC_DESTRUCT',
        '_EnumDestructablesInCircleBJMultiple_ScriptName=EnumDestructablesInCircleBJ',
         ]

         block[0] is the declaration line for the symbol, while block[1:] are lines for accessory parameters.

        :param block:
        :type block: list
        :return:
        :rtype: dict
        """

        kwargs = {'name': get_line_key(block[0])}
        return kwargs

    def convert_to_block(self):
        return "%s=%s" % (self.name, ','.join((str(param) for param in self.params())))
