# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import glob
from wand.image import Image
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
import os
import re
import sys

def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
    ap.add_argument('-i', '--inputfile',
                    help="inputfile",
                    default= "SWR2 Feature-2019-12-04.html")
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "Scans_VKvragenlijst23")
    ap.add_argument('-o', '--outputdir',
                    help="outputdir",
                    default="Scans_VKvragenlijst23_split")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
    outputdir = args['outputdir']
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    allFiles = {}
    all_files = glob.glob(inputdir + "/*.tif")
    for f in all_files:
        basename = os.path.basename(f)
        stderr(basename)
        ny = Image(filename = f)
        ny_converted = ny.convert('jpg')
        basename = basename.replace('.tif','.jpg')
        ny_converted.save(filename = f'{outputdir}/{basename}')

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

