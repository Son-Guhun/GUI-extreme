from collections import Iterator
import abc


from utilities import get_line_param, get_line_data
from my_collections import ValidatedDict
from we_object import TriggerEditorObject
from blockparameters import parse_block_parameter


BLOCK_PARAMETERS_ALL = {'Defaults', 'Limits', 'Category', 'ScriptName'}
BLOCK_PARAMETERS_NO_SCRIPTNAME = BLOCK_PARAMETERS_ALL - {'ScriptName'}


class TriggerEditorFunction(TriggerEditorObject):
    """
    This class represents a TriggerEditorObject that generates a JASS function. These kinds objects aren't necessarily
    declared in a single line, but also have blocks which are lines preceded by an underscore below it. A block ends on
    the next line that does not start in an underscore.

    Block parameters are represented by the classes in the blockparameters module.
    """
    _VALID_BLOCK_PARAMETERS = BLOCK_PARAMETERS_ALL

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.block_params = ValidatedDict(self._VALID_BLOCK_PARAMETERS)
        for param in self._VALID_BLOCK_PARAMETERS:
            if param in kwargs:
                self.block_params[param] = kwargs[param]

        try:
            self.argument_types = kwargs['argument_types']
        except KeyError:
            self.argument_types = []

        super(TriggerEditorFunction, self).__init__(**kwargs)

    @classmethod
    def supports(cls, keyword_arg):
        # type: (basestring) -> bool
        """According to testing, TriggerEvents and TriggerCalls do not support the Scriptname block parameter."""
        return keyword_arg in cls._VALID_BLOCK_PARAMETERS

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerEditorFunction, TriggerEditorFunction).parse_from_text(block)

        for line in block[1:]:
            param = get_line_param(line)
            kwargs[param] = parse_block_parameter(param, get_line_data(line))

        return kwargs

    def convert_to_block(self):
        return "%s=%s\n%s" % (self.name, ','.join((str(x) for x in self.params())), '\n'.join(self.block_params_str()))

    def block_params_str(self):
        return (("_%s_%s=%s" % (self.name, param, str(value))) for param, value in self.block_params.items())


# ======================================================================================================================
# Utilities
# ======================================================================================================================

def iter_all_functions():
    # type: () -> Iterator[TriggerEditorFunction]
    function_classes = [TriggerEditorFunction] + list(TriggerEditorFunction.get_subclasses())

    for class_ in function_classes:
        if class_.supports('Category'):
            for function_ in class_.get_class_instances():
                yield function_
