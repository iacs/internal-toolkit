#!/bin/env python3

# Commands
# ffmpeg -ss starting_time -t seconds -i input_file -vf f'fps={framerate}, scale={vscale}:-1:flags=split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse' -loop 0 output_file

import sys
import subprocess


def main():
    if len(sys.argv) < 7:
        print_usage()
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    starting_time = sys.argv[3]
    seconds = sys.argv[4]
    framerate = sys.argv[5]
    vscale = sys.argv[6]

    convert_cmd = [
        "ffmpeg",
        "-ss",
        starting_time,
        "-t",
        seconds,
        "-i",
        input_file,
        "-filter_complex",
        f"[0:v]fps={framerate},scale={
            vscale}:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse",
        "-loop",
        "0",
        output_file
    ]

    subprocess.run(convert_cmd)


def print_usage():
    print(f"""
        Usage: {sys.argv[0]} input output starting_time seconds framerate vscale

          input - input file
          output - output file
          starting_time - when to start trimming
          seconds - how many seconds to grab
          framerate - target frame rate e.g. 15
          vscale - scale gif vertically to this size in px e.g. 320
    """)


if __name__ == "__main__":
    main()
