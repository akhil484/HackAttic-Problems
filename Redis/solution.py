#https://hackattic.com/challenges/the_redis_one

import json
import requests
import base64
import redis


if __name__ == '__main__':
    #Get the data from URL
    response = requests.get('https://hackattic.com/challenges/the_redis_one/problem?access_token=')
    data = json.loads(response.text)
    base64_message = data['rdb']
    check_type_of = data['requirements']

    #decode
    rdb_bytes = base64.b64decode(base64_message)
    
    print(rdb_bytes)

    print(check_type_of)
    if rdb_bytes.startswith(b"mySQL"):
        print("Yesssssssssss")
        rdb_bytes = rdb_bytes.replace(b"mySQL", b"REDIS", 1)
    elif rdb_bytes.startswith(b"MYSQL"):
        print("Nooooooooooooooooooo")
        rdb_bytes = rdb_bytes.replace(b"MYSQL", b"REDIS", 1)
    elif rdb_bytes.startswith(b"mysql"):
        print("Nooooooooooooooooooo")
        rdb_bytes = rdb_bytes.replace(b"mysql", b"REDIS", 1)
    print('-----------------------')
    print(rdb_bytes)
    with open("dumps/dump.rdb", "wb") as f:
        f.write(rdb_bytes)

    # result = {}
    # result['db_count'] = 16
    # result['emoji_key_value'] = ""
    # result['expiry_millis'] = 
    # result['little_dawn'] =  "hash"
    # response = requests.post('https://hackattic.com/challenges/visual_basic_math/solve?access_token={access_token}', json={'result':result})
    # print(response.text)