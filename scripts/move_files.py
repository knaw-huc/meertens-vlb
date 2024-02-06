# -*- coding: utf-8 -*-
import argparse
import csv
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import os
import re
import shutil
import sys


def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description="")
    ap.add_argument('-d', '--input',
                    help="input csv",
                    default= "vlb-records-20240129-split_problems.csv")
    ap.add_argument('-b', '--backup',
                    help="backup dir",
                    default= "backup")
    ap.add_argument('-n', '--newfiles',
                    help="dir with new files",
                    default= "new")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputfile = args['input']
    backup = args['backup']
    newfiles = args['newfiles']
    teller = 0

    # backup old files
    with open(inputfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            source = row[2][7:]
            dest = source.replace('resources',backup)
            dest_dir = ('/').join(dest.split('/')[:-1])
            try:
                os.makedirs(dest_dir)
            except FileExistsError:
                pass
            try:
                shutil.move(source,dest_dir)
            except FileNotFoundError:
                stderr(f'{source} not found')

    # copy new files
    with open(inputfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dest = row[2][7:]
            source = dest.replace('resources',newfiles)
            dest_dir = ('/').join(dest.split('/')[:-1])
            # destination dirs always exist
            try:
                shutil.move(source,dest_dir)
            except FileNotFoundError:
                stderr(f'{source} not found')

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

