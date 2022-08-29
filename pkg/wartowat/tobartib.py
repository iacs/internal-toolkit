import sys
import json

from datetime import datetime, timezone


def main(argv):
    file_path = argv[0]
    data = _loadfile(file_path)
    convert_log_to_bartib_line(data)


def convert_log_to_bartib_line(data):
    for entry in data:
        project = entry['project']
        tags = entry['tags']
        start_time = _get_date(entry['start'])
        stop_time = _get_date(entry['stop'])
        if len(tags) == 0:
            tags = ["working"]
        tagstr = ", ".join(tags)
        result = f'{start_time} - {stop_time} | {project} | {tagstr}'
        print(result)


def _get_date(str_date):
    timew_fmt = '%Y%m%dT%H%M%SZ'
    out_fmt = '%Y-%m-%d %H:%M'
    # to_date = datetime.strptime(str_date, timew_fmt)
    to_date = datetime.fromisoformat(str_date)
    to_date = to_date.replace(tzinfo=timezone.utc)
    return to_date.strftime(out_fmt)


def _loadfile(fpath):
    with open(fpath, 'r') as jsonfile:
        return json.load(jsonfile)


if __name__ == '__main__':
    main(sys.argv[1:])
