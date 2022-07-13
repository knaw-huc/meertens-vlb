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
    ap = argparse.ArgumentParser(description='Convert multi page pdf's into single jpeg files and split the pages into left and right (if the page width is larger than the height)')
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "Scans_microfiches")
    ap.add_argument('-o', '--outputdir',
                    help="outputdir",
                    default="Scans_microfiches_split")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
    outputdir = args['outputdir']
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
    outdirlr = f'{outputdir}_lr'
    if not os.path.isdir(outdirlr):
        os.mkdir(outdirlr)

    allFiles = {}
    all_files = glob.glob(inputdir + "/*.pdf")
    for f in all_files:
        basename = os.path.basename(f)
        stderr(basename)
        ny = Image(filename = f)
        ny_converted = ny.convert('jpg')
        basename = basename.replace('.pdf','.jpg')
        ny_converted.save(filename = f'{outputdir}/{basename}')


    all_files = glob.glob(outputdir + "/*.jpg")
    for f in all_files:
        stderr(f)
        ny = Image(filename = f)
        if ny.height>ny.width:
            stderr(f'{f} is single page?')
            continue
        half = int(ny.width / 2)
        ny.crop(0, 0, half, ny.height)
        fileout = f.replace('.jpg','_links.jpg')
        fileout = fileout.replace(outputdir,outdirlr)
        ny.save(filename = fileout)
        #
        ny = Image(filename = f)
        half = int(ny.width / 2)
        ny.crop(half+1, 0, ny.width, ny.height)
        fileout = f.replace('.jpg','_rechts.jpg')
        fileout = fileout.replace(outputdir,outdirlr)
        ny.save(filename = fileout)

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

