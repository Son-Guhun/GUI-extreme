import abc


class TriggerEditorReferable:
    """
    An abstract class that represents an object which can be referenced by other objects within TriggerData.txt.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_referenced(self):
        pass

    @abc.abstractmethod
    def get_references(self):
        pass
