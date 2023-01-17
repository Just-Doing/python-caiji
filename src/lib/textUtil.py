import re

def text4FileName(str):
  regex = r'[?*/\|.:><]'
  return re.sub(regex, "", str)
