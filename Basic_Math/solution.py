#https://hackattic.com/challenges/visual_basic_math

import json
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai


try:
    
    genai.configure(api_key="{api_key}")
except ValueError as e:
    print(e)
    
    exit()


def get_image_from_url(url):
    try:
       
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  
        
       
        content_type = response.headers.get('content-type')
        if not content_type or 'image' not in content_type:
            print(f"Warning: URL did not return an image. Content-Type: {content_type}")
            return None
            
        return Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {e}")
        return None

def extract_text_from_image_url(image_url, prompt):
  
    model = genai.GenerativeModel('gemini-1.5-flash')

    image = get_image_from_url(image_url)
    

    try:
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"
    
def get_result(res, exp):
    exp = exp.strip()
    op = exp[0]
    exp = int(exp[1:])
    if op == '+':
        res = res + exp
    elif op == '-':
        res = res - exp
    elif op == 'x':
        res = res * exp
    else:
        res = res//exp
    return res

def calculate(extracted_text):
    result = 0
    
    expression = ''
    for text in extracted_text:
        expression += text
        if text == "\n":
            result = get_result(result, expression)
            expression = ''
 
    print(result)



    response = requests.post('https://hackattic.com/challenges/visual_basic_math/solve?access_token={access_token}', json={'result':result})
    print(response.text)


if __name__ == '__main__':
    #Get the data from URL
    response = requests.get('https://hackattic.com/challenges/visual_basic_math/problem?access_token={access_token}')
    data = json.loads(response.text)
    print(data['image_url'])
    image_url = data['image_url']
    

    prompt_text = "Perform OCR on this image. Extract all the numbers and mathematical symbols, line by line, exactly as they appear. Do not describe the image."

    
    extracted_text = extract_text_from_image_url(image_url, prompt_text)
    calculate(extracted_text)

    