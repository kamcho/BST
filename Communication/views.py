from django.shortcuts import render

# Create your views here.


import base64
 
# Replace these with your actual api_key and api_secret
api_key = 'your_api_key'
api_secret = 'your_api_secret'

def generate_leopard_token():
    # Combine api_key and api_secret with a colon
    credentials = f'{api_key}:{api_secret}'
    
    # Convert the combined string to base64 encoding
    base64_credentials = base64.b64encode(credentials.encode()).decode()
    
    # Include base64_credentials in the authorization header
    headers = {
        'Authorization': f'Basic {base64_credentials}'
    }
    return base64_credentials
 
# Now you can use the 'headers' dictionary in your API request
