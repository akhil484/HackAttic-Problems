import requests
import json
import base64
import psycopg2
import time


post_url = 'https://hackattic.com/challenges/backup_restore/solve?access_token={access_token}'

response = requests.get("https://hackattic.com/challenges/backup_restore/problem?access_token={access_token}")

data=json.loads(response.text)
base64_message = data['dump']
message_bytes = base64.b64decode(base64_message)


f = open('./data.dump', 'wb')
f.write(message_bytes)
f.close()

time.sleep(4)

#At this point I ran gunzip command to restore Database

conn = psycopg2.connect("dbname=dd user=akhil")
cur = conn.cursor()
  
cur.execute("SELECT ssn FROM criminal_records where status='alive';")
data = cur.fetchall()

# CLOSE THE CONNECTION
conn.close()
numbers=[]
for d in data:
	numbers.append(d[0])
solution = {'alive_ssns':numbers}
data=json.dumps(solution)
print(data)
solution_response = requests.post(post_url, data)
print(solution_response.text)
  

  
