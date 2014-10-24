#from twilio.rest import TwilioRestClient

#account_ssid = "AC62430b36d4cbf4f8075f46b70d2b1bc0"
#auth_token = "03ff2fa40b492e4da2fcbc840da1b03b"
#client = TwilioRestClient(account_ssid, auth_token)

#message = client.messages.create(to="+16509963472", from_="+1(408)675.5953", body = "hello there!")

from twilio.rest import TwilioRestClient

account_ssid = "AC62430b36d4cbf4f8075f46b70d2b1bc0"
auth_token = "03ff2fa40b492e4da2fcbc840da1b03b"
client = TwilioRestClient(account_ssid, auth_token)

# def text_this(number,message,test=False):
# 	if test:
# 		print "This would have sent a SMS to {}. Message: {}".format(number,message)
# 		return True
# 	text = client.messages.create(to=number, from_="+1(408)675.5953", body = message)


# text_this("16509963472","hello",True)


import requests
import random
r = requests.get('http://api.wunderground.com/api/8d854d9a85a461e1/conditions/q/CA/San_Francisco.json')

source_places = [('New York','NY'), ('San Francisco','CA'),('Seattle','WA'), ('Houston','TX')]


def get_random_place_name():
	return random.choice(source_places)

(city,state) = get_random_place_name()

j = r.json()
temperature = j['current_observation']['temperature_string']
def weather(city,state):
	return temperature
BASE_URL = 'http://api.wunderground.com/api/8d854d9a85a461e1/conditions/q' 
# def get_api_url(state,city):
# 	city = city.replace(" ", "_")
# 	return "{}/{}/{}".format(BASE_URL,state,city)
def forecast(state,city): 
	city = city.replace(" ", "_")
	return "{}/{}/{}.json".format(BASE_URL,state,city)

forecast_url = forecast('NY', 'New York')
print forecast_url
r = requests.get(forecast_url)
j = r.json()
temperature = j['current_observation']['temperature_string']
print temperature

#the_weather = weather(city,state)

