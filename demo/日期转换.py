#pip install python-dateutil

from dateutil.parser import parse
parse('Tue Sep 27 19:13:56 +0800 2022').strftime("%y-%m-%d %H:%M:%S")