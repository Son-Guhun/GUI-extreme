from my_collections import NameTracker

def get_line_data(line):
    return (line[line.find('=') + 1:].strip()).replace(' ', '')


def get_line_key(line):
    return (line[:line.find('=')].strip()).replace(' ', '')


def get_line_param(line):
    line = line[line.find('_')+1:]
    return line[line.find('_')+1:line.find('=')].strip()


class TriggerEditorObject(object):

    instances = NameTracker()

    def __init__(self, **kwargs):
        super(TriggerEditorObject, self).__init__()

        self.name = kwargs['name']
        TriggerEditorObject.instances[self.name] = self

    def __del__(self):
        del TriggerEditorObject.instances[self.name]

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        """
        Parses a symbol declaration block, passed as a list of strings, where each element is a line.

        Example:
        [
        'IsCustomCampaignButtonVisibile=1,0,boolean,integer',
         '_IsCustomCampaignButtonVisibile_Defaults=1',
         '_IsCustomCampaignButtonVisibile_Limits=1,_',
         '_IsCustomCampaignButtonVisibile_Category=TC_GAME'
         ]

         block[0] is the declaration line for the symbol, while block[1:] are lines for accessory parameters.

        :param block:
        :type block: list
        :return:
        :rtype: dict
        """

        kwargs = {'name': get_line_key(block[0])}
        return kwargs


class TriggerEditorFunction(TriggerEditorObject):

    supported_parameters = {'Defaults', 'Limits', 'Category', 'ScriptName'}

    def __init__(self, **kwargs):
        super(TriggerEditorFunction, self).__init__(**kwargs)

        if self.supports('Defaults') and 'Defaults' in kwargs:
            self.defaults = kwargs['Defaults']
        if self.supports('Limits') and 'Limits' in kwargs:
            self.limits = kwargs['Limits']
        if self.supports('Category') and 'Category' in kwargs:
            self.category = kwargs['Category']
        if self.supports('ScriptName') and 'ScriptName' in kwargs:
            self.script_name = kwargs['ScriptName']

    def supports(self, keyword_arg):
        return keyword_arg in type(self).supported_parameters

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerEditorFunction, TriggerEditorFunction).parse_from_text(block)

        for line in block[1:]:
            kwargs[get_line_param(line)] = get_line_data(line)

        for param in ('Defaults', 'Limits'):
            if param in kwargs:
                kwargs[param] = kwargs[param].split(',')

        return kwargs


class TriggerCategory(TriggerEditorObject):
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
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCategory, TriggerCategory).parse_from_text(block)

        params = get_line_data(block[0]).split(',')

        kwargs['display_text'] = params[0]
        kwargs['icon'] = params[1]
        kwargs['disable_display'] = int(params[2]) if len(params) > 2 else 0

        return kwargs


# Find [TriggerCalls] line and place these actions above it
class TriggerAction(TriggerEditorFunction):
    """
    [TriggerActions]
        Defines action functions
        Key: action function name
        Value 0: first game version in which this function is valid
        Value 1+: argument types
    """
    def __init__(self, **kwargs):
        super(TriggerAction, self).__init__(**kwargs)

        self.minimum_version = kwargs['minimum_version']
        self.argument_types = kwargs['argument_types']

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerAction, TriggerAction).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['argument_types'] = declaration[3:]

        return kwargs


class TriggerCall(TriggerEditorFunction):
    """
    [TriggerCalls]
        Defines function calls which may be used as parameter values
        Key: Function name
        Value 0: first game version in which this function is valid
        Value 1: flag (0 or 1) indicating if the call can be used in events
        Value 2: return type
        Value 3+: argument types

    Note: Operators are specially handled by the editor
    """

    supported_parameters = TriggerEditorFunction.supported_parameters - {'ScriptName'}

    def __init__(self, **kwargs):
        super(TriggerCall, self).__init__(**kwargs)

        self.minimum_version = kwargs['minimum_version']
        self.events_flag = kwargs['events_flag']
        self.return_type = kwargs['return_type']
        self.argument_types = kwargs['argument_types']

    @staticmethod
    def parse_from_text(block):
        # type: (list) -> dict
        kwargs = super(TriggerCall, TriggerCall).parse_from_text(block)

        declaration = get_line_data(block[0]).split(',')

        kwargs['minimum_version'] = int(declaration[0])
        kwargs['events_flag'] = int(declaration[1])
        kwargs['return_type'] = declaration[2]
        kwargs['argument_types'] = declaration[3:]

        return kwargs


a = ['IsCustomCampaignButtonVisibile=1,0,boolean,integer',
     '_IsCustomCampaignButtonVisibile_Defaults=1',
     '_IsCustomCampaignButtonVisibile_Limits=1,_',
     '_IsCustomCampaignButtonVisibile_Category=TC_GAME']


def b(my_class, block):
    return my_class(**my_class.parse_from_text(block))


my_dict = {
     u'TriggerCategories':        TriggerCategory,
     # u'TriggerTypes':             None,
     # u'TriggerTypeDefaults':      None,
     # u'TriggerParams':            None,
     # u'TriggerEvents':            None,
     # u'TriggerConditions':        None,
     u'TriggerActions':           TriggerAction,
     u'TriggerCalls':             TriggerCall,
     # u'DefaultTriggerCategories': None,
     # u'DefaultTriggers':          None
    }