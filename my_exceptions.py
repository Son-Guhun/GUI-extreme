from collections import Container


class TriggerSyntaxException(Exception):
    pass


class TriggerObjectInUseException(TriggerSyntaxException):
    """
    Args:
        msg (str): Human readable string describing the exception.
        usage_set (set[TriggerEditorObject]): A set of (all) objects which reference the object that raised the error.

    Attributes:
        msg (str): Human readable string describing the exception.
        usage_set (set[TriggerEditorObject]): A set of (all) objects which reference the object that raised the error.
    """

    # noinspection PySuperArguments,PyUnresolvedReferences
    def __init__(self, *args):
        # type: (str, Container) -> None
        super(TriggerObjectInUseException, self).__init__(self, *args)
        self._usage_set = args[1]

    @property
    def usage_set(self):
        return self._usage_set
    pass