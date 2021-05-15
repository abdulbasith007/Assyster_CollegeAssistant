import os
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
account_sid = 'ACe870fd97c5f66df8754e78f40d790dcb' #os.environ['TWILIO_ACCOUNT_SID']
auth_token = 'da039126252ba89a80e5f98cd25c6067' #os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)
def send_message(phone_number,mssage):
    client.api.account.messages.create(to=phone_number,from_="+14243836946",body=mssage)


    