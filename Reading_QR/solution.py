from urllib.request import urlopen
import json
import cv2
import requests


#Get the data from URL
response = urlopen('https://hackattic.com/challenges/reading_qr/problem?access_token={your_Access_Token}')
data = response.read()
data=json.loads(data)
print(data['image_url'])


#Download Image
r = requests.get(data['image_url'])
#wb so that Python doesn't make any changes to the data
with open("qrCode.jpg", "wb") as f:
    f.write(r.content)

#Decode the QR Code
d = cv2.QRCodeDetector()
a,b,c = d.detectAndDecode(cv2.imread("qrCode.jpg"))

#Post the data
requests.post('https://hackattic.com/challenges/reading_qr/solve?access_token={your_Access_Token}', json={'code':a})