# pip install requests
# pip install requests-oauthlib

# API secrets. NEVER share these with anyone!
CLIENT_KEY = "qmOBueiI8bk6zlywHNV1XBraJ"
CLIENT_SECRET = "YxW69HQElKmcobjSUtjE4eOE6yc41dNBSo2RYTUfMvL9gLqmrc"


API_URL = "https://api.twitter.com"
REQUEST_TOKEN_URL = API_URL + "/oauth/request_token"
AUTHORIZE_URL = API_URL + "/oauth/authorize?oauth_token={request_token}"
ACCESS_TOKEN_URL = API_URL + "/oauth/access_token"
TIMELINE_URL = API_URL + "/1.1/statuses/home_timeline.json"




import urlparse
import json
import requests
from requests_oauthlib import OAuth1


def get_request_token():
    """ Get a token allowing us to request user authorization """
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET)
    response = requests.post(REQUEST_TOKEN_URL,
                             auth=oauth)
    credentials = urlparse.parse_qs(response.content)

    request_token = credentials.get("oauth_token")[0]
    request_secret = credentials.get("oauth_token_secret")[0]
    return request_token, request_secret


def get_access_token(request_token, request_secret, verifier):
    """"
    Get a token which will allow us to make requests to the API
    """
    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=request_token,
                   resource_owner_secret=request_secret,
                   verifier=verifier)

    response = requests.post(ACCESS_TOKEN_URL, auth=oauth)
    credentials = urlparse.parse_qs(response.content)
    access_token = credentials.get('oauth_token')[0]
    access_secret = credentials.get('oauth_token_secret')[0]
    return access_token, access_secret


def get_user_authorization(request_token):
    """
    Redirect the user to authorize the client, and get them to give us the
    verification code.
    """
    authorize_url = AUTHORIZE_URL
    authorize_url = authorize_url.format(request_token=request_token)
    print 'Please go here and authorize: ' + authorize_url
    return raw_input('Please input the verifier: ')


def store_credentials(access_token, access_secret):
    """ Save our access credentials in a json file """
    with open("access.json", "w") as f:
        json.dump({"access_token": access_token,
                   "access_secret": access_secret}, f)


def get_stored_credentials():
    """ Try to retrieve stored access credentials from a json file """
    with open("access.json", "r") as f:
        credentials = json.load(f)
        return credentials["access_token"], credentials["access_secret"]


def authorize():
    """ A complete OAuth authentication flow """
    try:
        access_token, access_secret = get_stored_credentials()
    except IOError:
        request_token, request_secret = get_request_token()
        verifier = get_user_authorization(request_token)
        access_token, access_secret = get_access_token(request_token,
                                                       request_secret,
                                                       verifier)
        store_credentials(access_token, access_secret)

    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=access_token,
                   resource_owner_secret=access_secret)
    return oauth

TWEET_URL = API_URL + "/1.1/statuses/update.json"
def make_tweet(status_message,auth):
    data = {'status': status_message}
    response = requests.post(TWEET_URL, data=data, auth=auth)
    print response.json()
    print response.status_code
    return response



def get_user_location(user):
    return user['location']


def mentions1():
    auth = authorize()
    response = requests.get("https://api.twitter.com/1.1/statuses/mentions_timeline.json",auth=auth)
    j = response.json()
    for mentions in j: 
        username = mentions['user']['screen_name']
        text = mentions['text']
        print username, text

def user_recent_tweets(username, count):
    auth = authorize()
    response = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+username+"&count="+count,auth=auth)
    j = response.json()
    for tweet in j: 
        username = tweet['user']['screen_name']
        text = tweet['text']
        print username, text

def search_mentions(criteria, count):
    auth = authorize()
    response = requests.get("https://api.twitter.com/1.1/search/tweets.json?q="+criteria+"&count="+count,auth=auth)
    j = response.json()
    for tweet in j['statuses']:
        username = tweet['user']['screen_name']
        text = tweet['text']
        print username, text

def phrase_contains(to_check, target):
    if target.lower() in to_check.lower():
        return True
    else: 
        return False

def get_phrase_mentions(mentions,phrase):
    matching_users=[]
    for mention in mentions:
        text = mention['text']
        user = mention['user']
        location = get_user_location(user)
        if phrase_contains(text,phrase):
            matching_users.append(user)
            print matching_users
            print location
    return matching_users

def get_weather_mentions(mentions):
    return get_phrase_mentions(mentions,"What's the weather?")

def get_city_and_state(location):
    l = location.split(", ")
    if len(l)>1:
        return (l[0],l[1])
    else:
        return (l[0],"")

import requests
 
API_KEY = '9286261a1046d6b5'
BASE_URL = 'http://api.wunderground.com/api/{}/conditions/q/'.format(API_KEY)
 
def get_api_url(state, city):
    city = city.replace(" ", "_")
    return "{}/{}/{}.json".format(BASE_URL, state, city)
 
def check_weather(state, city):
    url = get_api_url(state, city)
    j = requests.get(url).json()
    try: 
        temperature = j['current_observation']['temperature_string']
    except KeyError:
        print "Error: Could not get current observation for city {}, {}!".format(city,state)
        return None
    return temperature

def get_weather_sentence(state,city):
    temp = check_weather(state, city)
    sentence = 'The weather in {} is {}.'.format(city, temp)
    return sentence

def tweet_reply(message, user, auth):
    username = user['screen_name']
    reply_message = "@{} You ask, I answer! {}".format(username, message)
    success = make_tweet(reply_message, auth)
    if success:
        print "Tweet was sent! {}".format(reply_message)
    else:
        print "Something went wrong. Boo! I was trying to send {}".format(reply_message)

def main():
    """ Main function """
    auth = authorize()
    # response = requests.get(TIMELINE_URL, auth=auth)
    # #print json.dumps(response.json(), indent=4)
    # j = response.json()
    # for tweet in j: 
    #     username = tweet['user']['screen_name']
    #     text = tweet['text']
    #     print username, text
    # mentions()
    # user_recent_tweets("cnn","10")
    # search_mentions("hackbright","10")
    #auth = authorize()
    response = requests.get("https://api.twitter.com/1.1/statuses/mentions_timeline.json", auth=auth)
    mentions = response.json()
    matching_users = get_weather_mentions(mentions)
    #return matching_users
    #make_tweet("tuesday night",auth)
    # print get_city_and_state("San Francisco, CA")
    # print get_city_and_state("New York, NY")
    # print get_city_and_state("Brighton, England")
    # print get_city_and_state("San Francisco")
    # print get_city_and_state("Your mom's house")
    for u in matching_users:
        location = get_user_location(u)
        (city,state) = get_city_and_state(location)
        sentence = get_weather_sentence(state,city)
        if sentence != '':
            tweet_reply(sentence,u,auth)
        else: 
            print "Could not tweet to {} as I have no weather to send".format(u['screen_name'])


if __name__=="__main__":
    main()