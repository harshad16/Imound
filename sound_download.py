import requests

# headers = {'content-disposition': 'attachment'}
# headers={'Authorization': 'Bearer 1n3SF3B1cXejCiQymF0fpsvNXitE7b'}
# auth= "BINhnaWONXGmeTBxc1xs4jozzvnuaU"
# url = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
# url_1 = 'https://freesound.org/apiv2/search/text/?query=piano&token=7W7CDnDfQeadgF30v2oPo4gBNFe2e6vXkg4r3TDg'

url = "http://10.25.55.250:5000/getImage"

video_file = open('images/airplane.jpg', 'rb')
payload = {'client_id': 1}
response = requests.post(url, files={'file': video_file},data=payload)
# r = requests.get(url_1)
print(response.status_code)
# print(r.json())

# for sound_detail in r.json().get('results'):
# 	print(sound_detail)
# 	break
# with open('movie.ogg', 'wb') as f:
#     f.write(r.content)




#curl -H "Authorization: Bearer 1n3SF3B1cXejCiQymF0fpsvNXitE7b" 'https://freesound.org/apiv2/sounds/14854/download/'
#curl "https://freesound.org/apiv2/search/text/?query=piano&token=7W7CDnDfQeadgF30v2oPo4gBNFe2e6vXkg4r3TDg"