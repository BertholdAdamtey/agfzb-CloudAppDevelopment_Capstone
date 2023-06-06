from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    return render(request, 'about.html')

# ...


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'contact.html')


# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index.html')  # Replace 'home' with the name of your home page URL pattern
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    
    return render(request, 'login.html')

# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('index.html')  # Replace 'home' with the name of your home page URL pattern


# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# def registration_request(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
        
#         # Check if the username or email already exists
#         if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#             return render(request, 'registration.html', {'error_message': 'Username or email already exists'})
        
#         # Create a new user
#         user = User.objects.create_user(username=username, password=password, email=email)
#         login(request, user)
#         return redirect('index')  # Replace 'home' with the name of your home page URL pattern
    
#     return render(request, 'registration.html')

# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://da9adc8a-0d7d-49a3-9047-364a337f4cf3-bluemix.cloudantnosqldb.appdomain.cloud"
        # Get dealers from the Cloudant DB
        context["dealerships"] = get_dealers_from_cf(url)

        # dealer_names = ' '.join([dealer.short_name for dealer in context["dealerships"]])
        # return HttpResponse(dealer_names)

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = dealer.review_set.all()  # Assuming you have a related model named `Review` for dealer reviews

    for review in reviews:
        review.sentiment = analyze_review_sentiments(review.review_text)  # Assign sentiment using analyze_review_sentiments

    return render(request, 'dealer_details.html', {'dealer': dealer, 'reviews': reviews})


# ..

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):

# from django.contrib.auth.decorators import login_required

# @login_required
def add_review(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        review = Review(dealer=dealer, rating=rating, comment=comment)

        # Append additional attributes to the review dictionary
        review_data = {
            "time": datetime.utcnow().isoformat(),
            "name": request.user.username,
            "dealership": dealer_id,
            "review": comment,
            "purchase": None  # Add any additional attributes you defined in your review-post cloud function
        }

        # Add the attributes to the review object
        for key, value in review_data.items():
            setattr(review, key, value)

        review.save()

         # Create the JSON payload
        json_payload = {
            "review": review
        }

        url = "https://your-api-url.com/post_review"
        response = post_request(url, json_payload, dealerId=dealer_id)

        # Print the response in the console
        print(response.json())

        return redirect('dealer_details', dealer_id=dealer_id)

    return render(request, 'add_review.html', {'dealer': dealer})

# ...



def registration_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error_message': 'Username or email already exists'})
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
        login(request, user)
        return redirect('index.html')  # Replace 'index' with the name of your home page URL pattern
    
    return render(request, 'registration.html')
