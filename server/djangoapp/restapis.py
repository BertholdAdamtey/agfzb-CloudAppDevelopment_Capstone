import requests
import json
from .models import CarDealer, DealerReview
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))



def post_request(url, json_payload, **kwargs):
    response = requests.post(url, json=json_payload, **kwargs)
    return response


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    # if api_key:
    #     # Basic authentication GET
    #     try:
    #      response = requests.get(url, headers={'Content-Type': 'application/json'},
    #                             params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    # # except:
    #         print("An error occurred while making GET request. ")
    # else:
    #     # No authentication GET
    #     try:
    #         response = requests.get(url, headers={'Content-Type': 'application/json'},
    #                                 params=kwargs)
    # except:
    #     # If any error occurs
    #     print("Network exception occurred")
    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    # json_data = json.loads(response.text)
    # return json_data
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("An error occurred while making GET request. ")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")

    # Retrieving the response status code and content
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(dealer_id):
    url = f"https://eu-de.functions.appdomain.cloud/api/v1/web/334d0dd7-f8d4-4bbf-a8b9-763e83ba4a2d/dealership-package/get_review/reviews?dealerId={dealer_id}"
    response = get_request(url, dealerId=dealer_id)

    reviews = []
    for review_data in response.json():
        dealership = review_data.get("dealership")
        name = review_data.get("name")
        purchase = review_data.get("purchase")
        review_text = review_data.get("review")  # Renamed 'review' variable to 'review_text'
        purchase_date = review_data.get("purchase_date")
        car_make = review_data.get("car_make")
        car_model = review_data.get("car_model")
        car_year = review_data.get("car_year")
        review_id = review_data.get("id")

        review = DealerReview(
            dealership,
            name,
            purchase,
            review_text,
            purchase_date,
            car_make,
            car_model,
            car_year,
            sentiment=None,  
            review_id=review_id
        )

        review.sentiment = analyze_review_sentiments(review_text)  # Assign sentiment using analyze_review_sentiments

        reviews.append(review)

    return reviews


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



def analyze_review_sentiments(dealerreview):
    url = "https://example.com/analyze_sentiments"
    api_key = "your_api_key"
    
    params = {
        "text": dealerreview,
        "version": "your_version",
        "features": "your_features",
        "return_analyzed_text": "your_return_analyzed_text"
    }

    response = get_request(url, params=params, api_key=api_key)
    # Process the response here

def get_request(url, params=None, api_key=None):
    headers = {
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth("apikey", api_key) if api_key else None

    response = requests.get(url, params=params, headers=headers, auth=auth)
    # Handle the response and return the result
    return response


