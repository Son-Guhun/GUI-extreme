"""
The classes contained in this module are used to represent block parameters of the Trigger Editor's functions types:

-TriggerEvents, TriggerConditions, TriggerActions and TriggerCalls


"""

import abc

# ======================================================================================================================
# Abstract and Generic classes
# ======================================================================================================================
from editorobjects import TriggerEditorObject


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

    # noinspection PyMissingConstructor
    def __init__(self, string):
        self._data = string.split(',')
        self._data = [x.strip() for x in self._data]

    def __str__(self):
        return ','.join(self._data)


class ParamCategory(BlockParameter):

    # noinspection PyMissingConstructor
    def __init__(self, string):
        self._data = TriggerEditorObject.get_object_from_name(string)

    def __str__(self):
        pass

    def __eq__(self, other):
        return self._data == other


class ParamLimits(ListParameter):
    pass


class ParamDefaults(ListParameter):
    pass

# ======================================================================================================================


_STRING_2_BLOCK_PARAM = {
    'Defaults':   ParamDefaults,
    'Limits':     ParamLimits,
    'Category':   ParamCategory,
    'ScriptName': str
}


def parse_block_parameter(parameter, string):
    try:
        return _STRING_2_BLOCK_PARAM[parameter](string)
    except KeyError as error:
        if parameter not in _STRING_2_BLOCK_PARAM:  # Make sure KeyError occurred in the right place.
            return string
        else:
            raise error
