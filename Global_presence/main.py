import functions_framework
import requests
import json
import os

@functions_framework.http
def make_presence_request(request):
    
    # Enable CORS for web requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        # Get the presence token from the request
        request_json = request.get_json()
        
        presence_token = request_json['presence_token']
        region = os.environ.get('FUNCTION_REGION', 'unknown')
        
        hackattic_url = f'https://hackattic.com/_/presence/{presence_token}'
        response = requests.get(hackattic_url, timeout=20)
        
        # Return the result
        return json.dumps({
            'success': True,
            'countries': response.text.strip(),
            'region': region,
            'status_code': response.status_code
        }), 200, headers
        
    except Exception as e:
        print(f"Error in {os.environ.get('FUNCTION_REGION', 'unknown')}: {str(e)}")
        return json.dumps({
            'error': str(e),
            'region': os.environ.get('FUNCTION_REGION', 'unknown')
        }), 500, headers