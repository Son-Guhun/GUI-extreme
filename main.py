import easygui
from my_exceptions import TriggerSyntaxException
import editorobjects as weobj
from collections import OrderedDict
from my_collections import BlockParser
import re
import io


def read_file(file_handle):
    contents = BlockParser()
    for line in file_handle:
        line = line[:line.find('//')]  #
        line = re.sub(r'\s+', '', line, flags=re.UNICODE)  # regex whitespace removal
        if line != '':
            if line[0] == '[':
                contents.set_category(line[1:-1])
            elif line[0] == '_':
                contents.append_line(line)
            else:
                contents.append_block()
                contents.append_line(line)
    return contents


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
