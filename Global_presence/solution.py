#https://hackattic.com/challenges/a_global_presence

import json
import requests


FUNCTION_URLS = ['https://asia-east1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-asia-east1',
'https://asia-south1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-asia-south1',
'https://australia-southeast1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-australia-southeast1',
'https://europe-west1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-europe-west1',
'https://southamerica-east1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-southamerica-east1',
'https://us-west1-optimal-buffer-473406-h7.cloudfunctions.net/global-presence-us-west1',
'https://hackattic-proxy.onrender.com/presence']

    

if __name__ == '__main__':
    #Get the data from URL
    response = requests.get('https://hackattic.com/challenges/a_global_presence/problem?access_token={access_token}')
    data = json.loads(response.text)
    presence_token = data['presence_token']
    print(presence_token)
    successful_requests = 0
    
    
    
    # call hackattic.com through each cloud function
    for i, function_url in enumerate(FUNCTION_URLS):
        region_name = function_url.split('//')[1].split('-')[0]
        
        try:
            
            # Send the presence_token to cloud function
            response = requests.post(function_url, 
                                    json={'presence_token': presence_token},
                                    timeout=25)
            
            result = response.json()
            
            print(f"   Response: {result}")
            if result.get('success'):
                countries = result.get('countries', '')
                region = result.get('region', 'unknown')
                successful_requests += 1
            
                
        except Exception as e:
            print(f'Request failed for {function_url}')
    

    
    if successful_requests >= 7:
        
        print('Post Solution')
        solution_response = requests.post(f'https://hackattic.com/challenges/a_global_presence/solve?access_token={access_token}', 
                                        json={})
        print(solution_response.text)
    else:
        print(f'Not enough successful requests. Need at least 7, got {successful_requests}')
    