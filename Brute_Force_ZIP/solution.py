#https://hackattic.com/challenges/brute_force_zip

import json
import zipfile
import os
import requests
import subprocess
import re


def main():
    #Get the data from URL
    response = requests.get('https://hackattic.com/challenges/brute_force_zip/problem?access_token={access_token}')
    data = json.loads(response.text)

    r = requests.get(data['zip_url'])

    with open("file.zip", "wb") as f:
        f.write(r.content)

    cmd = [
            "fcrackzip",
            "-u",
            "-v",
            "-b",
            "-c",
            "a1",
            "-l",
            "4-6",
            "file.zip"
        ]
    extract_to = "extracted/"

    try:
        # to run command
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        stdout = res.stdout + "\n" + res.stderr
        
        m = re.search(r"pw\s*==\s*([^\s]+)", stdout)
        print(m)
        if m:
            found = m.group(1).strip()
            with zipfile.ZipFile("file.zip", 'r') as z:
                z.extractall(extract_to, pwd=found.encode())
            print("Extraction completed!")
            with open("extracted/secret.txt", "r") as f:
                text = f.read().rstrip("\n")

            response = requests.post('https://hackattic.com/challenges/brute_force_zip/solve?access_token={access_token}', json={'secret':text})
            print(response.text)
        
    except Exception as e:
        print("Error Occured: ",e)

if __name__ == '__main__':
    main()