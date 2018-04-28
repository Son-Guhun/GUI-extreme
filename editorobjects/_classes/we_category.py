from collections import Iterator
from my_exceptions import TriggerObjectInUseException

from utilities import get_line_data
from we_object import TriggerEditorObject
from we_function import TriggerEditorFunction
from we_referable import TriggerEditorReferable


class TriggerCategory(TriggerEditorObject, TriggerEditorReferable):
    """
    [TriggerCategories]
        Defines categories for organizing trigger functions
        Key: Arbitrary category identifier
        Value 0: Display text
        Value 1: Icon image file
        Value 2: Optional flag (defaults to 0) indicating to disable display of category name
    """

    def __init__(self, **kwargs):
        super(TriggerCategory, self).__init__(**kwargs)

        self.display_text = kwargs['display_text']
        self.icon = kwargs['icon']
        self.disable_display = kwargs['disable_display'] if 'disable_display' in kwargs else 0

    @staticmethod
    def _get_functions():
        # type: () -> Iterator[TriggerEditorFunction]
        function_classes = [TriggerEditorFunction] + list(TriggerEditorFunction.get_subclasses())

        for class_ in function_classes:
            if class_.supports('Category'):
                for function_ in class_.get_class_instances():
                    yield function_

    def is_referenced(self):
        for function_ in self._get_functions():
            if function_.block_params['Category'] == self:
                return True
        return False

    def get_references(self):
        result = set()

        for function_ in self._get_functions():
            if function_.block_params['Category'] == self:
                result.add(function_)
        return result

    def remove(self):
        used_in = self.get_references()
        if used_in:
            raise TriggerObjectInUseException('Cannot remove ' + self._name + ' because it is referenced.', used_in)
        super(TriggerCategory, self).remove()

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCategory, TriggerCategory).parse_from_text(block)

        params = get_line_data(block[0]).split(',')

        kwargs['display_text'] = params[0]
        kwargs['icon'] = params[1]
        kwargs['disable_display'] = int(params[2]) if len(params) > 2 else 0

        return kwargs
