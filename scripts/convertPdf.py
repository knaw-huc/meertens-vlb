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
    ap = argparse.ArgumentParser(description="Convert multi page pdf's into single jpeg files and split the pages into left and right (if the page width is larger than the height)")
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "N7")
    ap.add_argument('-o', '--outputdir',
                    help="outputdir",
                    default="N7_split")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
    outputdir = args['outputdir']
    if inputdir != outputdir:
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)
        os.mkdir(outputdir)

    num_imgs = 0
    allFiles = {}
    all_files = glob.glob(inputdir + "/*.pdf")
    for f in all_files:
        basename = os.path.basename(f)
        img = Image(filename = f)
        img_converted = img.convert('jpg')
        basename = basename.replace('.pdf','.jpg')
        img_converted.save(filename = f'{outputdir}/{basename}')
        num_imgs = len(img_converted.sequence)
    orig_filename = all_files[0]


    all_files = glob.glob(outputdir + "/*.jpg")
    number = 0
    split_files = []
    basename = basename.replace('.jpg','')
    for num in range(num_imgs):
        f = f'{outputdir}/{basename}-{num}.jpg'
        number += 1
        img = Image(filename = f)
        if img.height>img.width:
            stderr(f'{f} is single page?')
            split_files.append(f)
            continue
        number += 1
        half = int(img.width / 2)
        img.crop(0, 0, half, img.height)
        fileout = f.replace('.jpg','_links.jpg')
        img.save(filename = fileout)
        split_files.append(fileout)
        stderr(fileout)
        #
        img = Image(filename = f)
        half = int(img.width / 2)
        img.crop(half+1, 0, img.width, img.height)
        fileout = f.replace('.jpg','_rechts.jpg')
        img.save(filename = fileout)
        split_files.append(fileout)
        stderr(fileout)
    num_imgs = len(split_files)
    basename = os.path.basename(orig_filename)
    with open(re.search(r'(^[^.]*).', os.path.basename(basename)).group(1)+'.xml','w') as uitvoer:
        uitvoer.write(makeCmdi(orig_filename,num_imgs,split_files))

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

