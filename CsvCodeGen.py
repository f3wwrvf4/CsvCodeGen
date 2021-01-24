#!/usr/bin/env python3
# CsvCodeGen.py

import pandas as pd
import os
import sys

from jinja2 import Template, Environment, FileSystemLoader

def Parse(header, line):
    tpl_root = 'TemplateFiles'

    data = dict(zip(header, line))

    tpl = line[0]
    tpl_path = os.path.join(tpl_root, tpl)

    env = Environment(loader=FileSystemLoader(tpl_root))
    template = env.get_template(tpl)

    return template.render(data)


def usage():
    print("""usage: CsvCodeGen.py [INPUT] [OUTPUT]""")

if __name__ == "__main__":
    args = sys.argv
    of = None
    try:
        df = pd.read_excel(args[1], header=None)

        if 2 < len(args):
            of = open(args[2], 'w')
    except:
        usage()
        exit(1)

    header = []
    for index, row_data in df.iterrows():
        raw_line = row_data.astype(str).values.tolist()
        line = [i for i in raw_line if i != 'nan']

#        print("line(" + str(index) + "):" + str(line))
        if not line:
            header = []
            pass
        else:
            if line[0][0] == '#':
                continue
            if not header:
                header = line
                pass
            else:
                result = Parse(header, raw_line)
                if of:
                    of.write(result)
                else:
                    print(result)


