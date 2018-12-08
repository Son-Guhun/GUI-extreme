# Find [TriggerCalls] line and place these actions above it
from utilities import get_line_data
from we_function import TriggerEditorFunction

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

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerAction, TriggerAction).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['argument_types'] = declaration[1:]

        return kwargs

    def block_params_str(self):
        r = []
        for param in self.block_params:
            r.append("_%s_%s=%s" % (self.name, param, self.block_params[param].value()))
        return '\n'.join(r)

    def convert_to_block(self):
        return """%s=%s
%s""" % (self.name, str(self.minimum_version) + ',' + ','.join(self.argument_types), self.block_params_str())
