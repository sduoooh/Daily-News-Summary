import time
from google import genai
from google.genai import types, errors

from config import GEMINI_API_KEY

def _get_ai_response(content):
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.95
            )
        )
        return response.text
    except errors.APIError as e:
        raise ValueError(f"AI Error: {e.message}")
    
def get_ai_response(content):
    retry_attempts = 3
    sleep_time = 2 
    
    while retry_attempts > 0:
        try:
            return _get_ai_response(content)
        except ValueError as e:
            time.sleep(sleep_time)
            retry_attempts -= 1
    raise e

def get_summary(items):
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    content = "\n".join([f"{item['publisher']} - {item['title']} - {item['date']}" for item in items]) 
    content = prompt.format(content)
    return get_ai_response(content)
