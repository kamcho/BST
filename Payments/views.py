import base64
import datetime
import json
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.db.models import Sum
import requests
from Charities.models import Charity, ChurchProjects
from .models import CharityPayments, InitiatedPayments, ProjectPayments
# Create your views here.
stk_push_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
transaction_status_url = 'https://api.safaricom.co.ke/mpesa/transactionstatus/v1/query'
def process_number(input_str):
    if input_str.startswith('0'):
        # Remove the leading '0' and replace it with '254'
        return '254' + input_str[1:]
    elif input_str.startswith('254'):
        # If it starts with '254', return the original string
        return input_str
    else:
        # If it doesn't start with either '0' or '254', return the original string
        return input_str

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

def initiate_payment(phone, amount, user, object_id, purpose):
    phone=process_number(phone)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    

    access_token = generate_access_token()
    password = generate_mpesa_password(timestamp)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    phone = '254742134431'
    payload = {
        "BusinessShortCode": 4161900,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": 4161900,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "Word.Saves",
        "TransactionDesc": "Payment TO Creamsons Analytics" 

    }

    response = requests.request("POST", stk_push_url, headers = headers, json = payload)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        print(data)
        checkout_id = data['CheckoutRequestID']
    
        payment = InitiatedPayments.objects.create(user=user, amount=amount, checkout_id=checkout_id,purpose=purpose, object_id=object_id)
    else:
        data = json.loads(response.text)
        print(data)
    
    

    return HttpResponse(response)




class DonateToCharity(TemplateView):
    template_name = 'Payments/donate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['charity_id']
        instance = self.kwargs['instance']
        if instance == 'Charity':
            charity = Charity.objects.get(id=id)
            contributions = CharityPayments.objects.filter(charity=charity)
        elif instance == 'Project':
            charity = ChurchProjects.objects.get(id=id)
            contributions = ProjectPayments.objects.filter(project=charity)

        totals = contributions.aggregate(totals=Sum('amount'))['totals']
        if not totals:
            totals = 0
        context['balance'] = charity.target - totals
        context['totals'] = totals
        context['charity'] = charity

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            amount = self.request.POST.get('amount')
            phone = self.request.POST.get('phone')
            user = self.request.user
            purpose = self.kwargs['instance']
            object_id = self.get_context_data().get('charity')
            object_id = object_id.id
            
            initiate_payment(phone, amount, user, object_id, purpose)

            return redirect(self.request.get_full_path())
