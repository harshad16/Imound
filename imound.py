import os
from PIL import Image

# convert images from all format tp jpeg 
def convertImg(filename):
	img = Image.open(filename)
	img.save(filename.split('.')[0]+'.jpeg')
	return filename.split('.')[0]+'.jpeg'

# get the labels of the image
def getlabel():
	pass

# get the sound from the api
def getsound():
	pass

# add the sound to the image
def addSoundtoImg():
	pass

def main():
	pass

if __name__ == '__main__':
	main()