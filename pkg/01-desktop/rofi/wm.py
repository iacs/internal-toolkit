#!/usr/bin/env python3
import subprocess as sp

menu = {
    "prompt": "WM operations",
    "options": [
        {
            "option": "Restart i3",
            "cmd": ["i3-msg", "restart"],
            "confirm":True
        },
        {
            "option": "Restart bars",
            "cmd": ["polybar-msg", "cmd", "restart"],
        }
    ]}


def run_rofi(options, prompt):
    # c = ['echo "{}" | rofi -dmenu -format i -i -p "{}"'.format( '\n'.join(options), prompt)]

    echo_cmd = ['echo', '\n'.join(options)]
    rofi_cmd = ['rofi', '-dmenu', '-format',
                'i', '-i', '-p', prompt, '-no-custom', '-a', '0']

    e_res = sp.Popen(echo_cmd, stdout=sp.PIPE)
    choice = sp.run(rofi_cmd, stdin=e_res.stdout,
                    stdout=sp.PIPE, encoding='utf-8')
    e_res.wait()
    return int(choice.stdout)


def main():
    data = menu
    opt_list = [x['option'] for x in data['options']]
    opt_data = data['options']
    print(opt_data)
    choice = run_rofi(opt_list, data['prompt'])
    if choice is not None:
        choice_data = opt_data[choice]
        if choice_data.get('confirm'):
            print('Confirm dtlg')
        sp.run(choice_data['cmd'])
        # print(choice)
        # print(opt_data[choice])


if __name__ == "__main__":
    main()
