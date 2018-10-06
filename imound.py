import os
import subprocess
import sys
import requests
from PIL import Image
from flask import Flask, render_template, request, session, flash, url_for, redirect, send_file


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
	sound_name=''
	mypath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'sound')
	onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	for file_name in onlyfiles:
		if label in file_name:
			sound_name = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'sound'),file_name)
			print(sound_name)
	if not sound_name:
		headers={'Authorization': 'Bearer 1n3SF3B1cXejCiQymF0fpsvNXitE7b'}
		search_url = 'https://freesound.org/apiv2/search/text/?query={}&token=7W7CDnDfQeadgF30v2oPo4gBNFe2e6vXkg4r3TDg'.format(label)
		res = requests.get(search_url)
		if res.status_code == 200:
			print(res.json().get('results'))
			for sound_detail in res.json().get('results'):
				print(sound_detail)
				sound_id = sound_detail.get('id')
				print("got the id:",sound_id)
				break

		download_url = 'https://freesound.org/apiv2/sounds/{}/download/'.format(sound_id)
		print(download_url)
		r = requests.get(download_url,headers=headers)
		print(r.status_code)
		with open(label+'.ogg', 'wb') as f:
			f.write(r.content)
		sound_name = label+'.ogg'
	return sound_name

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
		print(request.form)
		img_file = request.files['file']
		print(img_file)
		print(type(img_file))
		if img_file:
			filename = "img"
			img_file.save(filename)
			if filename:
		    		img_jpeg = convertImg(filename)
			elif sys.argv[1]:
				img_jpeg = convertImg(sys.argv[1])
			else:
				raise Exception()
			label = getlabel(img_jpeg)
			print("label",label)
			sound = getsound(label)
			print("sound",sound)
			video = addSoundtoImg(img_jpeg,sound,label)
			print("video",video)
			video_file = open(video, 'rb')
			if video_file:
				return send_file(video, mimetype='video/flv',as_attachment=True)
			else:
				return False

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000')
