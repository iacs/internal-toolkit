#!/usr/bin/env python3
# coding: utf-8
#
#  __     ______     ______     __  __     ______
# /\ \   /\  __ \   /\  ___\   /\ \/\ \   /\  ___\
# \ \ \  \ \  __ \  \ \ \____  \ \ \_\ \  \ \___  \
#  \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \/\_____\
#   \/_/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
# Harvester 1.0.3
# SN: 220515

import os
import json
import shutil
import subprocess


def main():
    try:
        options = load_data('options.json')
        files = options['files']
        sync_args = options['args_sync']
        arch_cmd = options['cmd_arch']
        sync_path = options.get('paths')['sync']
        arch_path = options.get('paths')['archive']
        sync_log_path = options.get('paths')['sync_log']
    except FileNotFoundError as err:
        try:
            shutil.copy('options_template.json', 'options.json')
        except FileNotFoundError as err:
            print('No options template found. Verify your installation')
            raise SystemExit
        print('No options file found. Please edit options.json with your settings')
        raise SystemExit
    except KeyError as err:
        print(f'Key undefined in options file: {err}')
        raise SystemExit

    arch_cmd = [x if x != '$DST' else arch_path for x in arch_cmd]
    create_filelist(files)
    sync(sync_path, sync_log_path, sync_args)
    runcmd(arch_cmd)
    runcmd(['rm', os.path.join(arch_path, 'harvest.7z')])
    move('harvest.7z', arch_path)


def load_data(path):
    data = {}
    with open(path, 'r', encoding='utf-8') as datafile:
        data = json.load(datafile)
    return data


def create_filelist(files_list):
    with open('filelist.txt', 'w') as filelist:
        files_list = map(lambda x: x + '\n', files_list)
        filelist.writelines(files_list)


def sync(sync_path, log_path, args):
    cmd_base = [
        'rsync',
        '-rvzh',
        '--checksum',
        '--delete',
        '--files-from=filelist.txt',
        '/',
        f'--log-file={log_path}',
        sync_path
    ]
    if len(args) > 0:
        cmd = cmd_base + args
    else:
        cmd = cmd_base

    subprocess.run(cmd)


def runcmd(command):
    if len(command) > 0:
        subprocess.run(command)


def move(source, destination):
    result = shutil.move(source, destination)
    print(f'Moved compressed archive to {destination}')


if __name__ == "__main__":
    main()
