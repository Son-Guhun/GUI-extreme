from utilities import get_line_data
from we_function import BLOCK_PARAMETERS_NO_SCRIPTNAME, TriggerEditorFunction


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

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCondition, TriggerCondition).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['argument_types'] = declaration[1:]

        return kwargs

    def __repr__(self):
        return """TriggerCondition(%s)
        MinVersion: %d
        Args: %s
        Block: 
        """ % (self.name,
               self.minimum_version,
               ",".join(self.argument_types))

