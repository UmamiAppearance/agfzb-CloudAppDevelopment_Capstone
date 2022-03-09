from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django import forms
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

DEALERSHIPS_API_URL = 'https://ffc4210a.us-south.apigw.appdomain.cloud/api/dealership'

# registration form
class RegistrationForm(forms.Form):
    '''Form class for user registration'''

    error_css_class = "error"
    
    username = forms.CharField(
        max_length = 30,
        label = 'Username',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter User Name:',
                'class': "form-control",
            },
        ),
    )
    first_name = forms.CharField(
        max_length = 30,
        label = 'First Name',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter First Name:',
                'class': "form-control",
            },
        ),
    )
    last_name = forms.CharField(
        max_length = 30,
        label = 'Last Name',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter Last Name:',
                'class': "form-control",
            },
        ),
    )
    password = forms.CharField(
        max_length = 30,
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter Password:',
                'class': "form-control",
            },
        ),
    )

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {
        "error": False 
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            context["error"] = True
            context["username"] = username
            context["password"] = password
    return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    registration_form = RegistrationForm()
    context = {
        'form': registration_form
    }
    return render(request, 'djangoapp/registration.html', context)

# Sign up view
def sign_up_request(request):
    if request.method != "POST":
        return redirect('djangoapp:register')

    registration_form = RegistrationForm(request.POST)

    if registration_form.is_valid():

        # get the cleaned form data 
        form_data = registration_form.cleaned_data
        
        user_exist = False

        try:
            # Check if user already exists
            User.objects.get(username=form_data['username'])
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(form_data['username']))
        
        # If it is a new user
        if not user_exist:

            # Create user in auth_user table
            user = User.objects.create_user(
                username=form_data['username'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                password=form_data['password']
            )

            # Login the user and redirect to index page
            login(request, user)    
            return redirect('djangoapp:index')
        else:
            
            # Add error message to the form
            registration_form.add_error("username", "The user already exists.")
    context = {
        'form': registration_form
    }
    return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = DEALERSHIPS_API_URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {
            'dealer_names': dealer_names,
        }
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

