from twilio.rest import Client

account_sid = 'ACca01c078b3ce1fafdd1d4ddeb3d9e917'
auth_token = '0511790693d9317144b45c628e9bcbc3'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='John 8:58 before abraham was, I AM',
  to='whatsapp:+254770392987'
)

print(message)