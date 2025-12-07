import os

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME') or 'gemini-2.5-flash'

SMTP_SERVER = os.getenv('SMTP_SERVER') or 'smtp.163.com'
SMTP_PORT = os.getenv('SMTP_PORT') or 465
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

ZAOBAO_SHADOW = os.getenv('ZAOBAO_SHADOW')
