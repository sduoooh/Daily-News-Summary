import time
from google import genai
from google.genai import types, errors

from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

class EmptyError(Exception):
    pass

class AIError(Exception):
    def __init__(self, message, original_error, empty_num):
        message = f"Summary empty {empty_num} times, error from AI: {original_error}\n\nThere are unhandled data:\n\n{message}"
        super().__init__(message)
        self.message = message

def _get_ai_response(prompt, content):
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.95,
                system_instruction=prompt
            )
        )
        res = response.text
        if not res or not res.strip():
            raise EmptyError()
        return res
    except errors.APIError as e:
        raise ValueError(f"Gemini API Error: code {e.code} - {e.message}")
    except EmptyError as e:
        raise EmptyError()

def get_ai_response(prompt, content):
    retry_attempts = 3
    sleep_time = 5 
    empty_num = 0
    error_info = ""

    while retry_attempts > 0:
        try:
            return _get_ai_response(prompt, content)
        except ValueError as e:
            time.sleep(sleep_time)
            retry_attempts -= 1
            error_info = e.args[0]
        except EmptyError as e:
            time.sleep(sleep_time)
            empty_num += 1
    print(f"AI returned empty response {empty_num} times.")
    raise AIError(content, error_info, empty_num)

def get_summary(items):
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    content = "\n".join([f"[{i+1}] {item['title']}({item['publisher']}), {item['date']}" for i, item in enumerate(items)]) 
    return get_ai_response(prompt, content)
