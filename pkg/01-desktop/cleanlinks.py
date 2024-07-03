#!/bin/env python3

import os

def main():
    all_files = os.listdir()
    for file in all_files:
        prfx = "Link to "
        if file.startswith(prfx):
            clean_name = file.removeprefix(prfx)
            os.rename(file, clean_name)
            print(f"orig: {file}, changed: {clean_name}")

if __name__ == "__main__":
    main()

