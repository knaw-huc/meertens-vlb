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

def getHeader():
    return '''<cmd:CMD
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cmd="http://www.clarin.eu/cmd/1" 
    xmlns:cmdp="http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1653377925727"
    CMDVersion="1.2" 
    xsi:schemaLocation="
      http://www.clarin.eu/cmd/1 https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd
      http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1653377925727 https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/clarin.eu:cr1:p_1653377925727/xsd">
    <cmd:Header>
        <cmd:MdProfile>clarin.eu:cr1:p_1653377925727</cmd:MdProfile>
    </cmd:Header>
'''

def getResources(base_name, number):
    pass

def getComponents(base_name, number):
    pass

def getFooter():
    return '</cmd:CMD>'

def makeCmdi(base_name, number):
    stderr(base_name)
    stderr(number)
    getHeader()
    getResources(base_name, number)
    getComponents(base_name, number)
    getFooter()

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

