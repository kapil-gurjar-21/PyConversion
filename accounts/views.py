from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import UserContactDetails
from .forms import UserContactRegistration
from django.core.mail import send_mail
from .task import * 
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from PyConversion import settings
from .kafka_logger import KafkaLogger
import environ
env = environ.Env()
environ.Env.read_env()



def home(request):
  return render(request,'base.html')


def aboutus(request):
  return render(request,'aboutus.html')

# User Contact Details 

def create_view(request):
    if request.method == 'POST':
        form = UserContactRegistration(request.POST)

        if form.is_valid():
            # Email Sending On User And Admin Mail Inbox
            recepient = str(form['user_email'].value())
            recepient_name = str(form['first_name'].value())

            configuration = sib_api_v3_sdk.Configuration()
            API_KEY = 'your-api-key'
            configuration.api_key['api-key'] = API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

            subject = "Welcome to PyConversion"
            html_content = "<html><body><h1>You Have Successfully Created Your Account</h1></body></html>"
            sender = {"name": "Your Name", "email": "example@gmail.com"}
            to = [{"email": recepient, "name": recepient_name}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender,
                                                          subject=subject)

            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                print(api_response)
            except ApiException as e:
                print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

            form.save()
            log_message = f"Item created"
            kafka_logger = KafkaLogger(bootstrap_servers='kafka:9092', topic='logs')
            kafka_logger.log_message(log_message)
            return redirect("home")
    else:
        form = UserContactRegistration()

    return render(request, 'createview.html', {'form': form})


# End Code User Contact Details 


def register_view(request):
  if request.method == "POST":
    pass