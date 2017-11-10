# django framework packages
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
# our own packages
from testapp.models import UserRequest, UserInfo
from allauth.socialaccount.models import SocialAccount, SocialToken

# installed & built-in packages
import argparse
import json
import logging
import os
import requests
import sys
import urllib
import yaml
import facebook

try:
    # for Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

logging.basicConfig(level=logging.DEBUG)
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


class TestView(TemplateView):
	template_name = ('home.html')


def index(request):
    logger.debug('Request data: {}'.format(request))
    return render(
        request,
        'home.html'
    )


def restaurants(request):
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

    response = {
        'restaurants': restaurants,
        'city': data[0],
        'term': data[1]
    }

    return render(
        request,
        'results.html',
        response
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
        logger.debug('No businesses for {0} in {1} found.'.format(term, location))
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
    access_token = SocialToken.objects.filter(account__user=user, account__provider='facebook').first()
    graph = facebook.GraphAPI(access_token=access_token, version=2.10)
    fb_user_info = graph.get_object(id='me', fields='name, location, hometown, work, likes, friends, education, religion, birthday, age_range')
    fb_info = ['name', 'location', 'hometown', 'friends', 'education', 'birthday', 'religion', 'age_range']
    fb_dict = {}
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
    

if __name__ == '__main__':
    main()
