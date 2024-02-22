import base64
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

# Generate Mpesa Password
def generate_access_token():
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    consumer_key = "aSG8gGG7GWSGapToKz8ySyALUx9zIdbBr1CHldVhyOLjJsCz"
    consumer_secret = "o8qwdbzapgcvOd1lsBOkKGCL4JwMQyG9ZmKlKC7uaLIc4FsRJFbzfV10EAoL0P6u"
    

    # make a get request using python requests liblary
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # return access_token from response
    if response.status_code == 200:
        access_token = response.json()['access_token']
        
        return access_token
    
    else:
        return None
    


import base64
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

def generate_mpesa_password(timestamp):
    # This is the deafult test number
    paybill = "174379" 
    timestamp = timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # this is the default test passkey
    pass_key = 'pass_key_goes_here' 
    concatenated_string = f"{paybill}{pass_key}{timestamp}"
    base64_encoded = base64.b64encode(concatenated_string.encode()).decode('utf-8')
    password = str(base64_encoded)

    return password


def initiate_stk_push():
    # Define the STK push endpoint URL
    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    # Get the current timestamp in the required format
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Set the headers for the HTTP request
    headers = {
        'Authorization': f'Bearer {generate_access_token()}',
        'Content-Type': 'application/json' }
    # Prepare the payload for the STK push request
    payload = {
        "BusinessShortCode": 174379,
        "Password": generate_mpesa_password(),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": '254742134431',
        "PartyB": 174379,
        "PhoneNumber": '254742134431',
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "Online.Store",
        "TransactionDesc": "Payment TO Online Store" 
    }
    # Make the POST request to initiate the STK push
    response = requests.post(stk_push_url, headers=headers, json=payload)
    # Check the HTTP status code of the response
    if response.status_code == 200:
        # Parse the JSON response data
        data = json.loads(response.text)
        return data
    else:
        # Return an error message for non-200 status codes
        return {'error': 'Failed to initiate STK push. Status Code:'}

    
    

    

