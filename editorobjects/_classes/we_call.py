from utilities import get_line_data
from we_function import TriggerEditorFunction, BLOCK_PARAMETERS_NO_SCRIPTNAME


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

    def params(self):
        yield self.minimum_version
        yield self.events_flag
        yield self.return_type
        for argtype in self.argument_types:
            yield argtype
