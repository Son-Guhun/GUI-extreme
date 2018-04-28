from typing import Dict, Iterator

from my_collections import NameTracker, ValidatedDict
from collections import OrderedDict
from my_exceptions import TriggerSyntaxException, TriggerObjectInUseException

import abc


# ======================================================================================================================
# region Utility Functions
# ======================================================================================================================
def get_line_data(line):
    return (line[line.find('=') + 1:].strip()).replace(' ', '')


def get_line_key(line):
    return (line[:line.find('=')].strip()).replace(' ', '')


def get_line_param(line):
    line = line[line.find('_')+1:]
    return line[line.find('_')+1:line.find('=')].strip()


# endregion
# ======================================================================================================================
# region Generic Classes
#
# These classes can represent more than 1 type of object within the trigger editor.
# ======================================================================================================================
class TriggerEditorObject(object):

    _instances = NameTracker()
    _class_sets = {}  # type: Dict[class, set]

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
        # type: () -> basestring
        return self._name

    @name.setter
    def name(self, new_name):
        # type: (basestring) -> None
        self._instances[new_name] = self  # Exception will be raised if the symbol is already taken.
        self.__del__()
        self._name = new_name

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
        try:
            return cls._instances[name]
        except KeyError:
            raise TriggerSyntaxException('Symbol '+name+' is not defined.')

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


BLOCK_PARAMETERS_ALL = {'Defaults', 'Limits', 'Category', 'ScriptName'}
BLOCK_PARAMETERS_NO_SCRIPTNAME = BLOCK_PARAMETERS_ALL - {'ScriptName'}


from blockparameters import parse_block_parameter
class TriggerEditorFunction(TriggerEditorObject):

    _VALID_BLOCK_PARAMETERS = BLOCK_PARAMETERS_ALL

    def __init__(self, **kwargs):
        self.block_params = ValidatedDict(self._VALID_BLOCK_PARAMETERS)
        for param in self._VALID_BLOCK_PARAMETERS:
            if param in kwargs:
                self.block_params[param] = kwargs[param]

        super(TriggerEditorFunction, self).__init__(**kwargs)

    @classmethod
    def supports(cls, keyword_arg):
        # type: (basestring) -> bool
        return keyword_arg in cls._VALID_BLOCK_PARAMETERS

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerEditorFunction, TriggerEditorFunction).parse_from_text(block)

        for line in block[1:]:
            param = get_line_param(line)
            kwargs[param] = parse_block_parameter(param, get_line_data(line))

        return kwargs


class TriggerEditorReferable:
    """
    An abstract class that represents an object which can be referenced by other objects within TriggerData.txt.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_referenced(self):
        pass

    @abc.abstractmethod
    def get_references(self):
        pass


# endregion
# ======================================================================================================================
# region Specific Classes
#
# These classes represent a single kind of object in the Trigger Editor.
# ======================================================================================================================
class TriggerCategory(TriggerEditorObject, TriggerEditorReferable):
    """
    [TriggerCategories]
        Defines categories for organizing trigger functions
        Key: Arbitrary category identifier
        Value 0: Display text
        Value 1: Icon image file
        Value 2: Optional flag (defaults to 0) indicating to disable display of category name
    """
    def __init__(self, **kwargs):
        super(TriggerCategory, self).__init__(**kwargs)

        self.display_text = kwargs['display_text']
        self.icon = kwargs['icon']
        self.disable_display = kwargs['disable_display'] if 'disable_display' in kwargs else 0

    @staticmethod
    def _get_functions():
        # type: () -> Iterator[TriggerEditorFunction]
        function_classes = [TriggerEditorFunction] + list(TriggerEditorFunction.get_subclasses())

        for class_ in function_classes:
            if class_.supports('Category'):
                for function_ in class_.get_class_instances():
                    yield function_

    def is_referenced(self):
        for function_ in self._get_functions():
            if function_.block_params['Category'] == self:
                return True
        return False

    def get_references(self):
        result = set()

        for function_ in self._get_functions():
            if function_.block_params['Category'] == self:
                result.add(function_)
        return result

    def remove(self):
        used_in = self.get_references()
        if used_in:
            raise TriggerObjectInUseException('Cannot remove '+self._name+' because it is referenced.', used_in)
        super(TriggerCategory, self).remove()

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCategory, TriggerCategory).parse_from_text(block)

        params = get_line_data(block[0]).split(',')

        kwargs['display_text'] = params[0]
        kwargs['icon'] = params[1]
        kwargs['disable_display'] = int(params[2]) if len(params) > 2 else 0

        return kwargs


class TriggerCondition(TriggerEditorFunction):
    """
    [TriggerConditions]
    // Defines boolean condition functions
    // Key: condition function name
    // Value 0: first game version in which this function is valid
    // Value 1+: argument types
    """

    _VALID_BLOCK_PARAMETERS = BLOCK_PARAMETERS_NO_SCRIPTNAME

    def __init__(self, **kwargs):
        super(TriggerCondition, self).__init__(**kwargs)

        self.minimum_version = kwargs['minimum_version']
        self.argument_types = kwargs['argument_types']

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCondition, TriggerCondition).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['argument_types'] = declaration[3:]

        return kwargs


# Find [TriggerCalls] line and place these actions above it
class TriggerAction(TriggerEditorFunction):
    """
    [TriggerActions]
        Defines action functions
        Key: action function name
        Value 0: first game version in which this function is valid
        Value 1+: argument types
    """
    def __init__(self, **kwargs):
        super(TriggerAction, self).__init__(**kwargs)

        self.minimum_version = kwargs['minimum_version']
        self.argument_types = kwargs['argument_types']

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerAction, TriggerAction).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['argument_types'] = declaration[3:]

        return kwargs


class TriggerCall(TriggerEditorFunction):
    """
    [TriggerCalls]
        Defines function calls which may be used as parameter values
        Key: Function name
        Value 0: first game version in which this function is valid
        Value 1: flag (0 or 1) indicating if the call can be used in events
        Value 2: return type
        Value 3+: argument types

    Note: Operators are specially handled by the editor
    """

    _VALID_BLOCK_PARAMETERS = BLOCK_PARAMETERS_NO_SCRIPTNAME

    def __init__(self, **kwargs):
        super(TriggerCall, self).__init__(**kwargs)

        self.minimum_version = kwargs['minimum_version']
        self.events_flag = kwargs['events_flag']
        self.return_type = kwargs['return_type']
        self.argument_types = kwargs['argument_types']

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCall, TriggerCall).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['events_flag'] = int(declaration[1])
        kwargs['return_type'] = declaration[2]
        kwargs['argument_types'] = declaration[3:]

        return kwargs


# endregion
# ======================================================================================================================
# region  Parser
# ======================================================================================================================
class TriggerEditorObjectParser(object):

    _DICT_STR2CLASS = OrderedDict({
        u'TriggerCategories':        TriggerCategory,
        # u'TriggerTypes':             None,
        # u'TriggerTypeDefaults':      None,
        # u'TriggerParams':            None,
        # u'TriggerEvents':            None,
        u'TriggerConditions':        TriggerCondition,
        u'TriggerActions':           TriggerAction,
        u'TriggerCalls':             TriggerCall,
        # u'DefaultTriggerCategories': None,
        # u'DefaultTriggers':          None
    })

    def __init__(self, string=''):
        self._class = None
        self._type_name = string
        if string:
            self.type_name = string

    def parse_block_to_object(self, block):
        return self._class(**self._class.parse_from_text(block))

    @property
    def type_name(self):
        return self._type_name

    @type_name.setter
    def type_name(self, string):
        try:
            self._class = self._DICT_STR2CLASS[string]
        except KeyError:
            raise TriggerSyntaxException("This trigger editor class is not recognized.")
        self._type_name = string
# endregion
# ======================================================================================================================


for subclass_ in TriggerEditorObject.get_subclasses():
    TriggerEditorObject._class_sets[subclass_] = set()
    TriggerEditorObject._class_sets[TriggerEditorObject] = set()
