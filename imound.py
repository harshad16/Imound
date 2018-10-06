import os
import subprocess
import sys
from PIL import Image


# convert images from all format tp jpeg 
def convertImg(filename):
	img = Image.open(filename)
	if(filename[-4:]!='jpeg'):
		img.save(filename.split('.')[0]+'.jpeg')
		filename = filename.split('.')[0]+'.jpeg'
	return filename

# get the labels of the image
def getlabel(filename):
	labels = subprocess.check_output('python3 classify_image.py --image_file '+filename+' --num_top_predictions=1',shell=True)
	labels = labels.decode("utf-8").split(',')
	return labels[0].replace(" ","")


# get the sound from the api
def getsound(label):
	
	pass

# add the sound to the image
def addSoundtoImg():
	pass

def main():
	img_jpeg = convertImg(sys.argv[1])
	label = getlabel(img_jpeg)
	sound = getsound(label)
	print(label)
	pass

if __name__ == '__main__':
	main()
