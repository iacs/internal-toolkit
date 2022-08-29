#!/usr/bin/python3
"""
Timewarrior to Watson CLI importer

Imports week files from timew to watson
"""

import os
import sys
import json
import subprocess
from datetime import datetime

PROJECT_TOKEN = '0.'


def main(argv):
    src_path = argv[0]
    weekfiles = get_files(src_path)
    allcmds = list()
    for f in weekfiles:
        data = loadfile(f)
        cmds = process_cmds(data)
        allcmds.extend(cmds)
    if len(allcmds) > 0:
        generate_script(src_path, allcmds)
        for f in weekfiles:
            mark_file(f)


def get_files(src_path):
    return [os.path.join(src_path, f) for f in os.listdir(src_path) if f.endswith('json')]


def process_cmds(data):
    timew_fmt = '%Y%m%dT%H%M%SZ'
    cmds = list()
    for frame in data:
        try:
            from_date = datetime.strptime(frame['start'], timew_fmt)
            to_date = datetime.strptime(frame['end'], timew_fmt)
            wtags = list()
            project = ""
            for tag in frame['tags']:
                if tag.startswith(PROJECT_TOKEN):
                    project = tag.split('.')[1]
                else:
                    wtags.append(f'+{tag}')
        except KeyError as err:
            print('Incorrect file format - cannot find key:', err)
            break
        except ValueError as err:
            print('Value error:', err)
            break
        cmd = [
            'watson',
            'add',
            '--from',
            f'"{from_date}"',
            '--to',
            f'"{to_date}"',
            project,
        ]
        cmd.extend(wtags)
        cmds.append(cmd)
    return cmds


def execute(cmds):
    for cmd in cmds:
        complete = subprocess.run(cmd)
        if complete.returncode != 0:
            print(f'command {cmd} returned with {complete.returncode}')
            return complete.returncode
    return 0


def generate_script(save_path, cmds):
    with open(os.path.join(save_path, 'import.sh'), 'w') as shellscript:
        shellscript.write('#!/bin/bash\n')
        shellscript.write('\n')
        for cmd in cmds:
            shellscript.write(' '.join(cmd))
            shellscript.write('\n')
    print(f'Import script written to {save_path}')


def loadfile(fpath):
    with open(fpath, 'r') as jsonfile:
        return json.load(jsonfile)


def mark_file(fpath):
    os.rename(fpath, f'{fpath}.spent')


if __name__ == '__main__':
    main(sys.argv[1:])
