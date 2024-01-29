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
    
    consumer_key = "lLznf101l98HUQTtb4AmPNQyneUiZvhb"
    consumer_secret = "6GaI08s5QvEHHfRV"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests liblary
    response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # return access_token from response
    if response.status_code == 200:
        access_token = response.json()['access_token'] 
        
        return access_token
    else:
        return JsonResponse({'error': 'Token generation failed'}, status=response.status_code)
    


def generate_mpesa_password(timestamp):
    paybill = "174379"

    consumer_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    concatenated_string = f"{paybill}{consumer_key}{timestamp}"
    base64_encoded = base64.b64encode(concatenated_string.encode()).decode('utf-8')
    password = str(base64_encoded)

    return str(base64_encoded)

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
         "BusinessShortCode": 174379,
    "Password": password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": phone,
    "PartyB": 174379,
    "PhoneNumber": phone,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 

    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        checkout_id = data['CheckoutRequestID']
    
        payment = InitiatedPayments.objects.create(user=user, amount=amount, checkout_id=checkout_id,purpose=purpose, object_id=object_id)
    
    

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
