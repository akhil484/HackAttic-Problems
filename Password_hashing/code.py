#https://hackattic.com/challenges/password_hashing

import json
import requests
import hashlib
import hmac
import base64


#Get the data from URL
response = requests.get('https://hackattic.com/challenges/password_hashing/problem?access_token=')
data = json.loads(response.text)
salt = base64.b64decode(data['salt'])
print(data)

password_bytes = data['password'].encode('utf-8')

salted_password = password_bytes + salt
sha256_hash = hashlib.sha256()
sha256_hash.update(salted_password)
hashed_password = sha256_hash.hexdigest()


hmac_obj = hmac.new(salt, password_bytes, hashlib.sha256)
hmac_hash = hmac_obj.hexdigest()


pbkdf_obj = hashlib.pbkdf2_hmac(data['pbkdf2']['hash'], password_bytes, salt, data['pbkdf2']['rounds'])
pbkdf_hash = pbkdf_obj.hex()


scrypt_obj = hashlib.scrypt(password_bytes, salt=salt, n=data['scrypt']['N'], r=data['scrypt']['r'], p=data['scrypt']['p'],maxmem=0, dklen=data['scrypt']['buflen'])
scrypt_hash = scrypt_obj.hex()



#Post the data
post_response = requests.post('https://hackattic.com/challenges/password_hashing/solve?access_token=8fc2793c26fbf04e', json={
'sha256':hashed_password, 'hmac': hmac_hash, 'pbkdf2': pbkdf_hash,'scrypt': scrypt_hash})

print(post_response)
print(post_response.text)
print(post_response.code)