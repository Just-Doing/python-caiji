import re
import json
from urllib.parse import quote_plus

src = img["src"]
pattern=re.compile("[\u4e00-\u9fa5]+")
for match in pattern.findall(src):
  src = src.replace(match, quote_plus(match))
print(src)