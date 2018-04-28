from utilities import get_line_param, get_line_data
from my_collections import ValidatedDict
from we_object import TriggerEditorObject
from blockparameters import parse_block_parameter


BLOCK_PARAMETERS_ALL = {'Defaults', 'Limits', 'Category', 'ScriptName'}
BLOCK_PARAMETERS_NO_SCRIPTNAME = BLOCK_PARAMETERS_ALL - {'ScriptName'}


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
