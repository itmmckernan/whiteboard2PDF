import io
import xml.etree.ElementTree as ET
import re
import sys
import os

from cairosvg import svg2png
from PIL import Image
import numpy as np

def addParentInfo(et):
    for child in et:
        child.attrib['__my_parent__'] = et
        addParentInfo(child)

def stripParentInfo(et):
    for child in et:
        child.attrib.pop('__my_parent__', 'None')
        stripParentInfo(child)

def getParent(et):
    if '__my_parent__' in et.attrib:
        return et.attrib['__my_parent__']
    else:
        return None

def svg(file):
    pages = []
    scaleRes = 5
    scaleFactor = 1
    offsetX = 0
    offsetY = 0
    root = ET.parse(file).getroot()
    addParentInfo(root)
    width = int(root.attrib["width"])*scaleRes
    height = int(root.attrib["height"])*scaleRes
    stream = io.BytesIO(svg2png(output_height=height, output_width=width, url=file))
    imageObj = Image.open(stream).copy()
    for image in root.findall(".//{http://www.w3.org/2000/svg}image"):
        #double parent
        list = []
        raw = getParent(getParent(image)).attrib['transform']
        for item in raw.split(",")[-3:]:
            list.append(float(re.sub(r'\)', '', item)))
        scaleFactor, offsetX, offsetY = [x*scaleRes for x in list]
        #child
        imageHeight = float(image.attrib["height"][:-2])*scaleFactor
        imageWidth = float(image.attrib["width"][:-2])*scaleFactor
        #single parent
        raw = getParent(image).attrib['transform']
        list2 = []
        for item in raw.split(",")[-2:]:
            list2.append(float(re.sub(r'\)', '', item))*scaleFactor)
        offset2X, offset2Y = list2
        #cropBox this shit
        corner1X = offsetX+offset2X
        corner1Y = offsetY+offset2Y
        #image = cv2.imread("5e3cb53a-9a27-4bd5-8da5-167786bc8412.png")
        #print({corner1X, corner1Y})
        cropped = np.array(imageObj)
        cropped = cropped[int(corner1Y):int(corner1Y+imageHeight), int(corner1X):int(corner1X+imageWidth)]
        #print(cropped.shape)
        page = Image.fromarray(cropped)
        pages.append(page)
        #page.show()
    pages[0].save("{}.pdf".format(os.path.basename(file).split(".")[0]), save_all=True, append_images=pages[1:], resolution=width/8.5)


for file in sys.argv[1:]:
    svg(file)