EMAIL_USE_TLS= True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'replacw with your email'
EMAIL_HOST_PASSWORD = 'replace with your password'
EMAIL_PORT = XXXX
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'replace with your email'
library_id = 'XXXXXXX'
library_type = 'user'
zoter_api_key = 'replace with your api-key'
open_ai_key = 'replace with your api-key'
header1  =  {
    'Content-Type': 'application/json',
    'x-api-key': 'replace with your api-key'
}
header2 =   {
             'Content-Type': 'application/json',
             'Authorization': f'Bearer {open_ai_key}'
            } 
api_url = 'https://api.openai.com/v1/chat/completions'
