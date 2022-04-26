from urllib import request
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from .forms import NewUserForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib import messages

#for password reset
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.db.models.query_utils import Q

from stats.apps import client, adafruitData
import sys
import os

from Adafruit_IO import MQTTClient

# Create your views here.
def register(response):
    return render(response, "register/register.html")

def register_request(request):
    # if request.method == "POST":        
    #     form = NewUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
            
    #         return redirect('/polls')
    #     else:
    #         print("abvfs")   
       
    # form = NewUserForm()
    # return render (request=request, template_name="register/register.html", context={"form":form})
    if request.method == "POST":
        username = request.POST.get('Email')
        if request.POST.get('Password1') == request.POST.get('Password2'):
            password =  request.POST.get('Password1')
            email = request.POST.get('Email')
            first_name = request.POST.get('First_name')
            last_name = request.POST.get('Last_name')
            user =  User.objects.create_user(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('register:login'))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, template_name="register/register.html")

def login_request(request):
    if request.method == "POST":
        username = request.POST.get("Email")
        password = request.POST.get("Password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_admin:
                login(request,user)
                return redirect(reverse('homepage:home_admin'))
            else:
                login(request,user)

                global client
                AIO_FEED_IDS = ['emotion-' + user.username, 'water-' + user.username]
                AIO_USERNAME = os.environ['AIO_USERNAME']
                AIO_KEY = os.environ['AIO_KEY']

                def connected(client):
                    print("Connection established successfully.")
                    if user.username not in adafruitData:
                        adafruitData[user.username] = {
                            'emotionData': [],
                            'waterData': [],
                        }
                    for feed in AIO_FEED_IDS:
                        client.subscribe(feed)

                def subscribe(client, userdata, mid, granted_qos):
                    print("Subscribed.")

                def disconnected(client):
                    print("Disconnected.")
                    sys.exit(1)

                def message(client, feed_id, payload):
                    global adafruitData                        
                    if feed_id == 'emotion-' + user.username:
                        adafruitData[user.username]['emotionData'].append(float(payload))
                    elif feed_id == 'water-' + user.username:
                        adafruitData[user.username]['waterData'].append(float(payload))

                client[0] = MQTTClient(AIO_USERNAME, AIO_KEY)
                client[0].on_connect = connected
                client[0].on_disconnect = disconnected
                client[0].on_message = message
                client[0].on_subscribe = subscribe
                client[0].connect()
                client[0].loop_background()

                return redirect(reverse('homepage:home'))
        messages.error(request, "The email or password is not correct.")
    return render(request, template_name="register/login.html")

def password_reset_request(request):
    if request.method == "POST":
        #password_reset_form = PasswordResetForm(request.POST)
        
        #if password_reset_form.is_valid():
            #data = password_reset_form.cleaned_data['email']
            data = request.POST.get("Email")
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    #password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html")#, context={"password_reset_form":password_reset_form})
                  
                
    

def logout_request(request):
    logout(request)
    return redirect(reverse('homepage:home'))