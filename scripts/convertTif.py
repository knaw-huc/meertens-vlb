# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import glob
from wand.image import Image
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL') 
from makeCmdi import makeCmdi
import os
import re
import sys
from pprint import pprint

def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
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
        img = Image(filename = f)
        img_converted = img.convert('jpg')
        basename = basename.replace('.tif','.jpg')
        img_converted.save(filename = f'{outputdir}/{basename}')
        pprint(vars(img_converted))
        num_imgs = len(img_converted.sequence)
        stderr(makeCmdi(f,num_imgs))
        exit(1)

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

