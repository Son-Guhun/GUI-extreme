# -*- coding: cp1252 -*-
"""
This exists because relative imports are fucking annyoing in Python
"""

import easygui

a = easygui.boolbox()

if a:
    a= easygui.textbox().replace('"','\\"')
else:
    a = (easygui.textbox().replace("\\n", "\n"))
    print a
    a = easygui.textbox(text=a).replace('"','\\"')


easygui.textbox(text=(a.replace("\n","\\n")))
