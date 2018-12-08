from collections import OrderedDict

from my_exceptions import TriggerSyntaxException
from we_type import TriggerType
from we_call import TriggerCall
from we_action import TriggerAction
from we_category import TriggerCategory
from we_condition import TriggerCondition


class TriggerEditorObjectParser(object):
    _DICT_STR2CLASS = OrderedDict({
        u'TriggerCategories': TriggerCategory,
        u'TriggerTypes':               TriggerType,
        # u'TriggerTypeDefaults':      None,
        # u'TriggerParams':            None,
        # u'TriggerEvents':            None,
        u'TriggerConditions':          TriggerCondition,
        u'TriggerActions':             TriggerAction,
        u'TriggerCalls':               TriggerCall,
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
