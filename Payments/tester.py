import base64
import datetime
import requests
from requests.auth import HTTPBasicAuth


access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


def generate_access_token():
    
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
    
def generate_mpesa_password(timestamp):
    paybill = "4161900"

    consumer_key = 'fa0e41448ce844d1a7a37553cee8bf22b61fec894e1ce3e9c0e32b1c6953b6d9'
    concatenated_string = f"{paybill}{consumer_key}{timestamp}"
    base64_encoded = base64.b64encode(concatenated_string.encode()).decode('utf-8')
    password = str(base64_encoded)

    return password
def get_status():
    lnmo_query_url =  "https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query"

    # Replace 'your_checkout_id' with the actual CheckoutRequestID you want to query
    checkout_id = "ws_CO_16022024034747715742134431"
    access_token = generate_access_token()
    # Set the request headers
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Set the request payload
    payload = {
        "BusinessShortCode": 4161900,
        "Password": generate_mpesa_password(timestamp),
        "Timestamp": timestamp,  # Replace with the current timestamp in the format YYYYMMDDHHMMSS
        "CheckoutRequestID": checkout_id
    }

    # Make the Lipa Na M-Pesa Online Query request
    response = requests.post(lnmo_query_url, json=payload, headers=headers)

    # Check the status of the response
    if response.status_code == 200:
        result = response.json()
        print("Transaction Status:", result.get("ResultCode"), "-", result.get("ResultDesc"))
    else:
        print("Error:", response.text)


get_status()