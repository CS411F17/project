# django framework packages
from django.shortcuts import render
from django.views.generic import TemplateView
# our own packages
from app.models import UserRequest, UserInfo
from allauth.socialaccount.models import SocialToken

# installed & built-in packages
import logging
import os
import requests
import sys
import yaml
import facebook
import ast
import random

# for Python 3.0 and later
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('VIEWS')

dirname = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dirname, "secrets.yaml")
with open(filename, 'r') as stream:
    try:
        yml = yaml.load(stream)
        logger.debug('Loaded secrets from yaml file')
    except yaml.YAMLError as e:
        logger.debug(e)

CLIENT_ID = yml['CLIENT_ID']
CLIENT_SECRET = yml['CLIENT_SECRET']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# default terms for debugging purposes
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Boston, MA'
# TODO: allow user to input how many search terms they want
SEARCH_LIMIT = 10


# TODO: Refactor this as a function
class TestView(TemplateView):
    template_name = ('home.html')


def index(request):
    logger.debug('Request data: {}'.format(request))
    return render(
        request,
        'home.html'
    )


def pure_luck(request):
    logger.debug('Request data: {}'.format(request))
    location = request.POST['location'].title()

    # taken from:
    # https://www.yelp.com/developers/documentation/v3/all_category_list
    # under the Food (all) list
    # XXX: Come up with a better way to store this
    categories = [
        'Acai Bowls',
        'Backshop',
        'Bagels',
        'Bakeries',
        'Beer, Wine & Spirits',
        'Bento',
        'Beverage Store',
        'Breweries',
        'Brewpubs',
        'Bubble Tea',
        'Butcher',
        'CSA',
        'Chimney Cakes',
        'Churros',
        'Cideries',
        'Coffee & Tea',
        'Coffee & Tea Supplies',
        'Coffee Roasteries',
        'Convenience Stores',
        'Cupcakes',
        'Custom Cakes',
        'Delicatessen',
        'Desserts',
        'Distilleries',
        'Do-It-Yourself Food',
        'Donairs',
        'Donuts',
        'Empanadas',
        'Ethical Grocery',
        'Farmers Market',
        'Fishmonger',
        'Food Delivery Services',
        'Food Trucks',
        'Friterie',
        'Gelato',
        'Grocery',
        'Hawker Centre',
        'Honey',
        'Ice Cream & Frozen Yogurt',
        'Imported Food',
        'International Grocery',
        'Internet Cafes',
        'Japanese Sweets',
        'Taiyaki',
        'Juice Bars & Smoothies',
        'Kiosk',
        'Kombucha',
        'Milkshake Bars',
        'Mulled Wine',
        'Nasi Lemak',
        'Organic Stores',
        'Panzerotti',
        'Parent Cafes',
        'Patisserie/Cake Shop',
        'Piadina',
        'Poke',
        'Pretzels',
        'Salumerie',
        'Shaved Ice',
        'Shaved Snow',
        'Smokehouse',
        'Specialty Food',
        'Candy Stores',
        'Cheese Shops',
        'Chocolatiers & Shops',
        'Dagashi',
        'Dried Fruit',
        'Frozen Food',
        'Fruits & Veggies',
        'Health Markets',
        'Herbs & Spices',
        'Macarons',
        'Meat Shops',
        'Olive Oil',
        'Pasta Shops',
        'Popcorn Shops',
        'Seafood Markets',
        'Tofu Shops',
        'Street Vendors',
        'Sugar Shacks',
        'Tea Rooms',
        'Torshi',
        'Tortillas',
        'Water Stores',
        'Wineries',
        'Wine Tasting Room',
        'Zapiekanka'
    ]

    term = random.choice(categories)
    data = [location, term]
    save_user_request(data)

    restaurants = yelp_call(term, location)
    key = random.choice(list(restaurants.keys()))
    single = restaurants[key]

    # XXX: Refactor this
    response = {
        'restaurants': {
            key: single,
        },
        'city': data[0],
        'term': data[1],
    }

    return render(
        request,
        'results.html',
        response
    )


def restaurants(request):
    user = request.user.id
    get_facebook_info(user)
    return render(
        request,
        'restaurants.html'
    )


def info(request):
    logger.debug('Restaurants: {}'.format(request.POST))
    city = request.POST['location'].title()
    term = request.POST['term']
    data = [city, term]

    save_user_request(data)

    restaurants = yelp_call(term, city)

    # check if filters are applied; if none are applied
    # then skip filtering_restaurants() call
    # also skip filtering_restaurants() call
    # if restaurants is None type to avoid error
    advanced_filters = [
        request.POST.getlist('group1[]'),
        request.POST.get('group2[]'),
        request.POST.get('group3[]')
    ]

    if (advanced_filters[0] == [] and advanced_filters[1] is None and advanced_filters[2] is None) \
       or restaurants is None:
            filtered_restaurants = restaurants
    else:
        filtered_restaurants = filtering_restaurants(request, restaurants)

    response = {
        'restaurants': filtered_restaurants,
        'city': data[0],
        'term': data[1],
    }

    return render(
        request,
        'results.html',
        response
    )


def final(request):
    #function to render user restaurant selection 
    picked_restaurant = request.POST.get("restaurant")
    #have to use ast library to convert because restaurant dict is passed as string by template
    rest_dict = ast.literal_eval(picked_restaurant)
    return render(
        request,
        'choice.html',
        {'restaurant': rest_dict},
    )


def save_user_request(data):
    user_request = UserRequest(location=data[0], term=data[1])
    user_request.save()
    logging.info('Saved user request data')


def obtain_bearer_token(host, path):
    """
    Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)

    try:
        bearer_token = response.json()['access_token']
    except KeyError as e:
        logger.debug("Invalid response: {}".format(e))

    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """
    Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    logger.debug('Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, location):
    """
    Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """
    Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
    response = search(bearer_token, term, location)
    businesses = response.get('businesses')

    if not businesses:
        logger.debug(
            'No businesses for {0} in {1} found.'.format(term, location)
        )
        return

    responses = {}
    for business in businesses:
        business_id = business['id']
        business_result = get_business(bearer_token, business_id)
        logger.debug('Result for business "{0}" found:'.format(business_id))
        logger.debug('{}'.format(business_result))
        responses[business_id] = business_result

    return responses


def yelp_call(keyTerm, location):
    try:
        returnData = query_api(keyTerm, location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return returnData


def get_facebook_info(user):
    access_token = SocialToken.objects.filter(
        account__user=user,
        account__provider='facebook'
    ).first()

    graph = facebook.GraphAPI(access_token=access_token, version=2.10)
    fb_info = ['name', 'location', 'hometown', 'friends', 'education', 'birthday', 'religion', 'age_range']

    fb_user_info = graph.get_object(
        id='me',
        fields=', '.join(fb_info)
    )

    user_info = UserInfo()
    for k in fb_user_info:
        if k in fb_info:
            if k == 'education':
                temp = fb_user_info['education']
                user_info.education = temp[-1]['school']['name']
            if k == 'location':
                user_info.location = fb_user_info['location']['name']
            if k == 'hometown':
                user_info.hometown = fb_user_info['hometown']['name']
            if k == 'friends':
                user_info.num_friends = fb_user_info['friends']['summary']['total_count']
            if k == 'name':
                user_info.name = fb_user_info['name']
            if k == 'age_range':
                user_info.age_range = fb_user_info['age_range']['min']
            if k == 'religion':
                user_info.religion = fb_user_info['religion']
    user_info.save()


def filtering_restaurants(request, restaurants):
    # restaurants search filters where [0] is price filter
    # [1] is rating filter
    # [2] is hours filter
    advanced_filters = [
        request.POST.getlist('group1[]'),
        request.POST.get('group2[]'),
        request.POST.get('group3[]')
    ]

    # initialize with 'checker' key to check filter initialization
    dict1 = {'checker': 'None'}  # price filtered dict
    dict2 = {'checker': 'None'}  # rating filtered dict
    dict3 = {'checker': 'None'}  # hours filtered dict

    # creating dictionaries with applied filters
    if advanced_filters[0] != []:
        dict1 = {
            restaurant_id: restaurant for restaurant_id, restaurant in restaurants.items()
            if restaurant['price'] in advanced_filters[0]
        }
    if advanced_filters[1] is not None:
        dict2 = {
            restaurant_id: restaurant for restaurant_id, restaurant in restaurants.items()
            if float(restaurant['rating']) >= float(advanced_filters[1])
        }
    if advanced_filters[2] is not None:
        dict3 = {
            restaurant_id: restaurant for restaurant_id, restaurant in restaurants.items()
            if restaurant['hours'][-1]['is_open_now'] is True
        }

    # combine included dict keys into list for processing
    keys_1 = []
    keys_1.append(set(dict1.keys()))
    keys_1.append(set(dict2.keys()))
    keys_1.append(set(dict3.keys()))

    # only include filters that are applied
    keys_lst = [keys for keys in keys_1 if 'checker' not in keys]

    # finding intersection of dictionary keys from applied advanced filters
    intersection = restaurants.keys()
    for k in keys_lst:
        intersection = intersection & k

    # generate final list of filtered dictionary results
    filtered_restaurants = {
        restaurant_id: restaurant for restaurant_id, restaurant in restaurants.items()
        if restaurant_id in intersection
    }

    return filtered_restaurants
