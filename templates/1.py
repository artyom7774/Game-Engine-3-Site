import re

import json

text = open("nodes.html", encoding="utf-8").read()

# Поиск всех совпадений между символами '&' (исключая сами символы)
matches = re.findall(r'&(.*?)&', text, re.DOTALL)

print("Найденные подстроки:")

a = {}
for idx, match in enumerate(matches, 1):
    a[match] = match

print(json.dumps(a, indent=4))
