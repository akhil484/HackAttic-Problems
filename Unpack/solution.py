#Problem link - https://hackattic.com/challenges/help_me_unpack

from urllib.request import urlopen
import json
import base64
import requests
from struct import *


#Get the data from URL
response = urlopen('https://hackattic.com/challenges/help_me_unpack/problem?access_token={your_access_token}')
data = response.read()
data=json.loads(data)

base64_message = data['bytes']

#decode
message_bytes = base64.b64decode(base64_message)
try:
    sign_int = unpack('i', message_bytes[0:4])[0]
    unsign_int = unpack('I', message_bytes[4:8])[0]
    dshort = unpack('h', message_bytes[8:10])[0]
    float_val = unpack('f', message_bytes[12:16])[0]
    doub_val = unpack('d', message_bytes[16:24])[0]
    end_doub = unpack('>d', message_bytes[24:])[0]
except Exception as e:
    print(e)


data = {}
data['int'] = sign_int
data['uint'] = unsign_int
data['short'] = dshort
data['float'] = float_val
data['double'] = doub_val
data['big_endian_double'] = end_doub

data=json.dumps(data)

#Post the data
print(requests.post('https://hackattic.com/challenges/help_me_unpack/solve?access_token={your_access_token}', data).text)