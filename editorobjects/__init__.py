# noinspection PyUnresolvedReferences
from _classes.we_object import TriggerEditorObject
# noinspection PyUnresolvedReferences
from _classes.we_function import TriggerEditorFunction
# noinspection PyUnresolvedReferences
from _classes.we_referable import TriggerEditorReferable
# noinspection PyUnresolvedReferences
from _classes.we_type import TriggerType
# noinspection PyUnresolvedReferences
from _classes.we_action import TriggerAction
# noinspection PyUnresolvedReferences
from _classes.we_category import TriggerCategory
# noinspection PyUnresolvedReferences
from _classes.we_condition import TriggerCondition
# noinspection PyUnresolvedReferences
from _classes.block_parser import TriggerEditorObjectParser
# noinspection PyUnresolvedReferences
from _classes.we_call import TriggerCall


for subclass_ in TriggerEditorObject.get_subclasses():
    TriggerEditorObject._class_sets[subclass_] = set()
    TriggerEditorObject._class_sets[TriggerEditorObject] = set()
