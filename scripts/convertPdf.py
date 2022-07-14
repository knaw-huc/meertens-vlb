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
    ap = argparse.ArgumentParser(description="Convert multi page pdf's into single jpeg files and split the pages into left and right (if the page width is larger than the height)")
    ap.add_argument('-d', '--inputdir',
                    help="inputdir",
                    default= "N7")
    ap.add_argument('-o', '--outputdir',
                    help="outputdir",
                    default="N7")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    stderr(datetime.today().strftime("start: %H:%M:%S"))
    args = arguments()
    inputdir = args['inputdir']
    outputdir = args['outputdir']
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
    #outdirlr = f'{outputdir}_lr'
    #if not os.path.isdir(outdirlr):
    #    os.mkdir(outdirlr)

    allFiles = {}
    all_files = glob.glob(inputdir + "/*.pdf")
    for f in all_files:
        basename = os.path.basename(f)
        stderr(basename)
        img = Image(filename = f)
        img_converted = img.convert('jpg')
        basename = basename.replace('.pdf','.jpg')
        img_converted.save(filename = f'{outputdir}/{basename}')
        num_imgs = len(img_converted.sequence)
        stderr(f'num imgs: {num_imgs}')
    save_filename = all_files[0]


    all_files = glob.glob(outputdir + "/*.jpg")
    number = 0
    split_files = []
    for f in all_files:
        number += 1
        img = Image(filename = f)
        if img.height>img.width:
            stderr(f'{f} is single page?')
            stderr(f)
            split_files.append(f)
            # save file name
            continue
        number += 1
        half = int(img.width / 2)
        img.crop(0, 0, half, img.height)
        fileout = f.replace('.jpg','_links.jpg')
        #fileout = fileout.replace(outputdir,outdirlr)
        img.save(filename = fileout)
        split_files.append(fileout)
        stderr(fileout)
        #
        img = Image(filename = f)
        half = int(img.width / 2)
        img.crop(half+1, 0, img.width, img.height)
        fileout = f.replace('.jpg','_rechts.jpg')
        #fileout = fileout.replace(outputdir,outdirlr)
        img.save(filename = fileout)
        split_files.append(fileout)
        stderr(fileout)
        # remove split file?
    num_imgs = len(split_files)
    stderr(f'split_files: {num_imgs}')
    stderr(f'number: {number}')
    pprint(split_files)
    basename = os.path.basename(save_filename)
    with open(re.search(r'(^[^.]*).', os.path.basename(basename)).group(1)+'.xml','w') as uitvoer:
        uitvoer.write(makeCmdi(save_filename,num_imgs,split_files))

    stderr(datetime.today().strftime("einde: %H:%M:%S"))

