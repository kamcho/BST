import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse


access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate'


def generate_access_token():
    
    consumer_key = "aSG8gGG7GWSGapToKz8ySyALUx9zIdbBr1CHldVhyOLjJsCz"
    consumer_secret = "o8qwdbzapgcvOd1lsBOkKGCL4JwMQyG9ZmKlKC7uaLIc4FsRJFbzfV10EAoL0P6u"
    

    # make a get request using python requests liblary
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # return access_token from response
    if response.status_code == 200:
        print(response,'\n\n')
        access_token = response.json() 
        print(access_token)
        
        return "access_token"
    
    else:
        print('hey token',response.text,'\n\n')
        return JsonResponse({'error': 'Token generation failed'}, status=response.status_code)
    
generate_access_token()
