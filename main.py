import easygui
from my_exceptions import TriggerSyntaxException
import editorobjects as weobj
import editorpackages as wepakg
from collections import OrderedDict
from my_collections import BlockParser
import re
import io


def minimize_line(string):
    # type: (str) -> str
    """Removes all comments and whitespace from a line."""

    string_uncommented = string[:string.find('//')]

    # regex whitespace removal => don't remove whitespaces that are between quotation marks
    # https://stackoverflow.com/questions/9577930/regular-expression-to-select-all-whitespace-that-isnt-in-quotes
    return re.sub(r'\s+(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)', '', string_uncommented, flags=re.UNICODE)


INDICATOR_CATEGORY = '['
INDICATOR_BLOCK_MEMBER = '_'


def read_file(file_handle):
    contents = BlockParser()
    for line in file_handle:
        line = minimize_line(line)
        if line != '':
            if line[0] == INDICATOR_CATEGORY:
                contents.new_category(line[1:-1])
            elif line[0] == INDICATOR_BLOCK_MEMBER:
                contents.add_line(line)
            else:
                contents.new_block()
                contents.add_line(line)
    return contents


if __name__ == "__main__":
    with io.open('a.txt', 'r', encoding="utf-8-sig") as f:
        blocks = read_file(f)

    data = OrderedDict()
    for we_type in blocks:
        try:
            parser = weobj.TriggerEditorObjectParser(we_type)
        except TriggerSyntaxException:
            continue
        data[we_type] = OrderedDict()
        for block in blocks[we_type]:
            # temp = parser.parse_block_to_object(block)
            try:
                temp = parser.parse_block_to_object(block)
            except TriggerSyntaxException as e:
                print block
                print e.message
                continue
            data[we_type][temp.name] = temp

    a = data.keys()
    easygui.choicebox('Hello', 'Choices', data[a[1]].keys())

    for name in data['TriggerCategories']:
        print name
        print data['TriggerCategories'][name].is_referenced()

    user_package = wepakg.TriggerEditorPackage()


"""
with open("b.txt","w") as f:
    for a in data:
        f.write("[{}]\n\n\n\n".format(a))
        for n in data[a]:
            f.write(data[a][n].convert_to_block() + '\n')
"""
