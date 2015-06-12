# imports/modules
import os
import random
import json
import collections
from PIL import Image

# Convert (r, g, b) into #rrggbb color
def getRGBstring( (r, g, b) ):
	s = "#"
	s = s + format(r, '02x')
	s = s + format(g, '02x')
	s = s + format(b, '02x')
	return s
	
def getFreqData(img):
    w, h = img.size
    pixels = img.load()
    freq = collections.Counter()
    
    for x in range(w):
        for y in range(h):
            color = getRGBstring( pixels[x, y] )
            freq[ color ] += 1
            
    return freq
    


def do_compute():
	# Open the image
    origImgFile = 'res/bryce.jpg'
    origImg = Image.open(origImgFile)


	# Process the image
    freq = getFreqData(origImg)



    # freq:
    #   { "#rrggbb": 100,
    #     "#33ff22": 200,
    #     "#66aa9c": 300,
    #     ...
    #    }
    
	# Save the processed information
    output = { 'file': origImgFile,
	           'freq': freq }
	
    f = open("res/freq.json",'w')
    s = json.dumps(output, indent = 4)
    f.write(s)
	
	

