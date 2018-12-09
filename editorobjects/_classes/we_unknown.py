from we_object import TriggerEditorObject


class TriggerEditorUnknown(TriggerEditorObject):

    def params(self):
        yield None

    def __init__(self, **kwargs):
        self._block = kwargs['unknown_block']
        super(TriggerEditorUnknown, self).__init__(**kwargs)

    def __del__(self):
        self.remove()

    def remove(self):
        del self._instances[self._name]
        self._class_sets[type(self)].remove(self)

    def __str__(self):
        return self._name

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
        kwargs = super(TriggerEditorUnknown, TriggerEditorUnknown).parse_from_text(block)

        kwargs['unknown_block'] = block
        return kwargs

    def convert_to_block(self):
        return "\n".join(self._block)
