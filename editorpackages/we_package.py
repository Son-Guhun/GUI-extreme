from editorobjects import TriggerEditorObject


class TriggerEditorPackage(object):

    def __init__(self):
        self._objects = set()

    def unload(self):
        """
        Removes all TriggerEditorObjects inside the package from the package itself and global namespace.
        """
        for weobj in self._objects:
            weobj.remove()
        self._objects.clear()

    def remove(self, package):
        """
        Removes a TriggerEditorObject from the package and from the global namespace.

        :type package: basestring, TriggerEditorObject
        """
        if isinstance(package, basestring):
            package = TriggerEditorObject.get_object_from_name(package)  # type: TriggerEditorObject

        self._objects.remove(package)
        package.remove()

