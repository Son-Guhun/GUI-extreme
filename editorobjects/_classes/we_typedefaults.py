from utilities import get_line_data, get_line_key
from we_object import TriggerEditorObject


class TriggerTypeDefault(TriggerEditorObject):

    def __init__(self, **kwargs):
        super(TriggerTypeDefault, self).__init__(**kwargs)
        self.script_text = kwargs['script_text']
        self.display_text = kwargs['display_text'] if 'display_text' in kwargs else None

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
        kwargs = {'name': get_line_key(block[0])+"_DEFAULT_",
                  'script_text': declaration[0]}
        if len(declaration) > 1:
            kwargs['display_text'] = declaration[1]
        return kwargs

    def params(self):
        yield self.script_text
        if self.display_text:
            yield self.display_text

    def convert_to_block(self):
        return "%s=%s" % (self.name.replace("_DEFAULT_", ""), ','.join((str(param) for param in self.params())))
