import re
from dataparser import apply_func_to_file

def regex_test(text_file):
    text = text_file.read()
    matches = re.findall(r"\d\d:\d\d", text)
    print(matches)
    print(type(matches))
    print(matches[1])

apply_func_to_file(regex_test, "data/tramlines.txt")

# Bra video: https://youtu.be/sa-TUpSx1JA
# Han har också fler om regex just i python, har inte tittat på allt själv men finns iaf vilket är nice