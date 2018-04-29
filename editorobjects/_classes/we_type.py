from we_function import iter_all_functions
from utilities import get_line_data
from we_object import TriggerEditorObject
from we_referable import TriggerEditorReferable


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

        self.minimum_version = kwargs['minimum_version']
        self.is_global = kwargs['is_global']
        self.comparable = kwargs['comparable']
        self.display_name = kwargs['display_name']
        self.base_type = kwargs['base_type'] if 'base_type' in kwargs else None
        self.import_type = kwargs['import_type'] if 'import_type' in kwargs else None
        self.treat_as_base = kwargs['treat_as_base'] if 'treat_as_base' in kwargs else None

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
            kwargs['treat_as_base'] = declaration[6]
        except IndexError:
            pass

        return kwargs
