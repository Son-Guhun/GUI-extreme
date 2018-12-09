from we_function import iter_all_functions
from utilities import get_line_data
from we_object import TriggerEditorObject
from we_referable import TriggerEditorReferable
from my_types import IntBool, WC3Version


class TriggerType(TriggerEditorObject, TriggerEditorReferable):
    """
    [TriggerTypes]
        Defines all trigger variable types to be used by the Script Editor
        Key: type name
        Value 0: first game version in which this type is valid
        Value 1: flag (0 or 1) indicating if this type can be a global variable
        Value 2: flag (0 or 1) indicating if this type can be used with comparison operators
        Value 3: string to display in the editor
        Value 4: base type, used only for custom types
        Value 5: import type, for strings which represent files (optional)
        Value 6: flag (0 or 1) indicating to treat this type as the base type in the editor
    """

    def __init__(self, **kwargs):
        super(TriggerType, self).__init__(**kwargs)

        self.minimum_version = WC3Version(kwargs['minimum_version'])
        self.is_global = IntBool(kwargs['is_global'])
        self.comparable = IntBool(kwargs['comparable'])
        self.display_name = kwargs['display_name']
        self.base_type = kwargs['base_type'] if 'base_type' in kwargs else None
        self.import_type = kwargs['import_type'] if 'import_type' in kwargs else None
        self.treat_as_base = IntBool(kwargs['treat_as_base']) if 'treat_as_base' in kwargs else None

    def params(self):
        yield self.minimum_version
        yield self.is_global
        yield self.comparable
        yield self.display_name
        if self.base_type:
            yield self.base_type
        if self.import_type:
            yield self.import_type
        if self.treat_as_base:
            yield self.treat_as_base

    def is_referenced(self):
        for function_ in iter_all_functions():
            if self.name in function_.argument_types:
                return True
        return False

    def get_references(self):
        result = set()
        for function_ in iter_all_functions():
            if self.name in function_.argument_types:
                result.add(function_)
        return result

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerType, TriggerType).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = declaration[0]
        kwargs['is_global'] = declaration[1]
        kwargs['comparable'] = declaration[2]
        kwargs['display_name'] = declaration[3]
        try:
            kwargs['base_type'] = declaration[4]
            kwargs['import_type'] = declaration[5]
            kwargs['treat_as_base'] = declaration[6]  # TODO: Test what this does and see if it works with all types
        except IndexError:
            # Index error occurred because optional parameters were not declared!
            pass

        return kwargs
