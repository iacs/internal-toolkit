#!/usr/bin/env python

import sys
import datetime
import subprocess

from math import floor


def main():
    secs_in_hour = 60 * 60
    secs_in_day = secs_in_hour * 24
    cmd = ["grep", "full system upgrade", "/var/log/pacman.log"]
    output = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')
    try:
        line = output.split('\n')[-2].split(' ')[0][1:-1]
        dtobj = datetime.datetime.fromisoformat(line).replace(tzinfo=None)
        dtnow = datetime.datetime.now()
        delta = dtnow - dtobj
        if delta.days == 2:
            print(f'{delta.days} days ago')
            sys.exit(0)
        if delta.days >= 3:
            print(f'{delta.days} days ago')
            sys.exit(1)
        tot_seconds = delta.days * secs_in_day + delta.seconds
        if tot_seconds < secs_in_hour * 2:
            mins = floor(delta.seconds/60)
            print(f'{mins} mins ago')
            sys.exit(0)
        if tot_seconds < secs_in_day * 2:
            hours = floor(tot_seconds / secs_in_hour)
            print(f'{hours} hours ago')
            sys.exit(0)
    except ValueError:
        print("Nothing yet")
        sys.exit(-1)


if __name__ == "__main__":
    main()
