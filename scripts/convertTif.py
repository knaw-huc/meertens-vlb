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
import shutil
import sys

def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description='Convert multi page tif files into single page jpeg files"')
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "VKvragenlijst23")
#    ap.add_argument('-o', '--outputdir',
#                    help="outputdir",
#                    default="VKvragenlijst23_split")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
#    outputdir = args['outputdir']
#    if not os.path.isdir(outputdir):
#        os.mkdir(outputdir)

    allFiles = {}
    all_files = glob.glob(inputdir + "/*.tif")
    for f in all_files:
        basename = os.path.basename(f)
        outputdir = f"{inputdir}/{basename.replace('.tif','')}"
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)
        os.mkdir(outputdir)
        img = Image(filename = f)
        img_converted = img.convert('jpg')
        basename = basename.replace('.tif','')
        img_converted.save(filename = f'{outputdir}/{basename}-%03d.jpg')
        num_imgs = len(img_converted.sequence)
        all_files = glob.glob(outputdir + "/*.jpg")
        with open(inputdir + '/' + re.search(r'(^[^.]*).', os.path.basename(basename)).group(1)+'.xml','w') as uitvoer:
            uitvoer.write(makeCmdi(inputdir,f,num_imgs,all_files))

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

