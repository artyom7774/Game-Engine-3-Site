import re

import json

text = open("programming.html", encoding="utf-8").read()

matches = re.findall(r'&(.*?)&', text, re.DOTALL)

a = {}
for idx, match in enumerate(matches, 1):
    a[match] = match

print(json.dumps(a, indent=4))
