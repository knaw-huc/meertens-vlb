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

def split_left_right(basename,num_imgs,inputdir,outputdir):
    all_files = glob.glob(outputdir + "/*.jpg")
    number = 0
    split_files = []
    logfile = open(f'{inputdir}/{basename}.log','w')
    for n in range(num_imgs):
        num = f'{n:03}'
        f = f'{outputdir}/{basename}-{num}.jpg'
        number += 1
        img = Image(filename = f)
        if img.height>img.width:
            logfile.write(f'{f} is single page?\n')
            split_files.append(f)
            continue
        number += 1
        half = int(img.width / 2)
        img.crop(0, 0, half, img.height)
        fileout = f.replace('.jpg','_links.jpg')
        img.save(filename = fileout)
        split_files.append(fileout)
        logfile.write(f'{fileout}\n')
        #
        img = Image(filename = f)
        half = int(img.width / 2)
        img.crop(half+1, 0, img.width, img.height)
        fileout = f.replace('.jpg','_rechts.jpg')
        img.save(filename = fileout)
        split_files.append(fileout)
        logfile.write(f'{fileout}\n')
    num_imgs = len(split_files)
    with open(f'{inputdir}/{basename}.xml','w') as uitvoer:
        uitvoer.write(makeCmdi(basename,num_imgs,split_files))



def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")

def arguments():
    ap = argparse.ArgumentParser(description="Convert multi page pdf's into single jpeg files and split the pages into left and right (if the page width is larger than the height)")
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "N7")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
    num_imgs = 0
    allFiles = {}
    all_files = glob.glob(inputdir + "/*.pdf")
    for f in all_files:
        basename = os.path.basename(f).replace('.pdf','')
        outputdir = f"{inputdir}/{basename}"
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)
        os.mkdir(outputdir)
        img = Image(filename = f)
        img_converted = img.convert('jpg')
        img_converted.save(filename = f'{outputdir}/{basename}-%03d.jpg')
        num_imgs = len(img_converted.sequence)
        split_left_right(basename,num_imgs,inputdir,outputdir)

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

