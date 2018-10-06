import os
import subprocess
import sys
import requests
from PIL import Image
from flask import Flask, render_template, request, session, flash, url_for, redirect


app = Flask(__name__)


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
	return labels[0].replace(" ","").split("(")[0]


# get the sound from the api
def getsound(label):
	search_url = 'https://freesound.org/apiv2/search/text/?query={}&token=7W7CDnDfQeadgF30v2oPo4gBNFe2e6vXkg4r3TDg'.format(label)
	res = requests.get(search_url)
	if res.status_code == 200:
		for sound_detail in res.json().get('results'):
			sound_id = sound_detail.get(id)
			print("got the id:",sound_id)
			break

	download_url = 'https://freesound.org/apiv2/sounds/{}/download/'.format(sound_id)

	r = requests.get(download_url,headers=headers)
	print(r.status_code)
	with open(label+'.ogg', 'wb') as f:
		f.write(r.content)
	return label+'.ogg'

# add the sound to the image
def addSoundtoImg(image,sound,label):
	#Img format is always jpeg, sound format is not known ffmpeg uses automatic best possible codec
	# If the frame rate and the codecs are not good change this line of code.
	os.system('ffmpeg -i '+image+' -i '+sound+' '+label+'.flv')
	return str(label)+'.flv'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/getImage', methods=['GET', 'POST'])
def main():
	print('welcome to imound')
	if request.method == 'POST':
		#print(request.body)
		print(request)
		img_file = request.files['file']
		print(img_file)
		print(type(img_file))
		if img_file:
        		filename = "aeroplane"
        		img_file.save(filename)
        

	img_jpeg = convertImg(sys.argv[1])
	label = getlabel(img_jpeg)
	print("label",label)
	sound = getsound(label)
	print("sound",sound)
	video = addSoundtoImg(img_jpeg,sound,label)
	print("video",video)
	video_file = open(video, 'rb')
	response = requests.post(url, files={'file':video_file})
	print("Status_Code of return API:",response.status_code)
	if response.status_code == 200:
		return True
	else:
		return False

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000')
