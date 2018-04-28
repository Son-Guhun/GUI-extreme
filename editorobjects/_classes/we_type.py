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
        self.base_type = kwargs['base_type']
        self.import_type = kwargs['import_type']
        self.treat_as_base = kwargs['treat_as_base']

    def is_referenced(self):
        pass

    def get_references(self):
        pass

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

        declaration = get_line_data(block[0]).split(',')

        kwargs = {'minimum_version': declaration[0],
                  'is_global': declaration[1],
                  'comparable': declaration[2],
                  'display_name': declaration[3],
                  'base_type': declaration[4],
                  'import_type': declaration[5],
                  'treat_as_base': declaration[6]
                  }
        return kwargs
