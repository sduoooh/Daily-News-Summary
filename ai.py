from google import genai
from google.genai import types, errors

from config import GEMINI_API_KEY

def get_ai_response(content):
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.95
            )
        )
    
    except errors.APIError as e:
        raise ValueError(f"AI Error: {e.message}")
    return response.text

def get_summary(items):
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    content = "\n".join([f"{item['publisher']} - {item['title']} - {item['date']}" for item in items]) 
    content = prompt.format(content)
    return get_ai_response(content)