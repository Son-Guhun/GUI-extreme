"""
The classes contained in this module are used to represent block parameters of the Trigger Editor's functions types:

-TriggerEvents, TriggerConditions, TriggerActions and TriggerCalls


"""

import abc

# ======================================================================================================================
# Abstract and Generic classes
# ======================================================================================================================
from we_object import TriggerEditorObject


class BlockParameter(object):
    """
    An abstract class that represents an object which can be referenced by other objects within TriggerData.txt.
    """
    __metaclass__ = abc.ABCMeta

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def __init__(self, string):
        # type: (str) -> None
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


# ======================================================================================================================
# Specific classes
# ======================================================================================================================
class ListParameter(BlockParameter):
    """Base class for block paramaters that are lists (Defaults and Limits)"""

    # noinspection PyMissingConstructor
    def __init__(self, string):
        self._data = string.split(',')
        self._data = [x.strip() for x in self._data]

    def __str__(self):
        return ','.join(self._data)

    __repr__ = __str__

    def value(self):
        return ",".join(self._data)


class ParamCategory(BlockParameter):
    """This is the category where the TriggerEditorObject appears in inside the Editor."""

    # noinspection PyMissingConstructor
    def __init__(self, string):
        self._data = TriggerEditorObject.get_object_from_name(string)

    def __str__(self):
        return self._data.name

    def __eq__(self, other):
        return self._data == other

    __repr__ = __str__

    @staticmethod
    def type():
        return "Category"

    def value(self):
        return self._data.name


class ParamLimits(ListParameter):
    @staticmethod
    def type():
        return "Limits"


class ParamDefaults(ListParameter):
    @staticmethod
    def type():
        return "Defaults"

# ======================================================================================================================


_STRING_2_BLOCK_PARAM = {
    'Defaults':   ParamDefaults,
    'Limits':     ParamLimits,
    'Category':   ParamCategory,
    'ScriptName': str
}


def parse_block_parameter(parameter, string):
    """Converts a block parameter to the correct class.
    :param parameter: This is the name of the parameter (Category, Defaults, Limits).
    :param string:  This is the string passed as the parameter.
    :return: If no appropriate class exists, a simple string is returned.
    """
    try:
        return _STRING_2_BLOCK_PARAM[parameter](string)
    except KeyError as error:
        if parameter not in _STRING_2_BLOCK_PARAM:  # Make sure KeyError occurred in the right place.
            return string
        else:
            raise error
