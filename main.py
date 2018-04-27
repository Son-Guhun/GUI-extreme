import easygui
from my_exceptions import TriggerSyntaxException
import editorobjects as weobj
from collections import OrderedDict

import io


def read_block(text_list):
    block = []
    block_found = False
    for i in xrange(len(text_list)):
        line = text_list[i]
        line = line[:line.find('//')]
        if line.strip() != '':
            if line[0] != '_':
                if block_found:
                    return block, i
                else:
                    block_found = True
                    block.append(line)
            else:
                if block_found:
                    block.append(line)
                else:
                    raise TriggerSyntaxException('Block member found outside block!')
    return ()


# with io.open('TriggerData.txt', 'r', encoding="utf-8-sig") as f:
with io.open('a.txt', 'r', encoding="utf-8-sig") as f:
    a = f.readlines()

blocks = OrderedDict()

while True:
    block = read_block(a)
    if block:
        if block[0][0].strip()[0] == '[':
            string = block[0][0].strip()[1:-1]
            blocks[string] = []
        else:
            blocks[string].append(block[0])
        a = a[block[1]:]
    else:
        break

data = OrderedDict()
for we_type in blocks:
    try:
        parser = weobj.TriggerEditorObjectParser(we_type)
    except TriggerSyntaxException:
        continue
    data[we_type] = OrderedDict()
    for block in blocks[we_type]:
        temp = parser.parse_block_to_object(block)
        data[we_type][temp.name] = temp

a = data.keys()
easygui.choicebox('Hello', 'Choices', data[a[1]].keys())
