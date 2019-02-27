import requests
import os

geocoder_url = 'https://geocoder.api.here.com/6.2/geocode.json'
mapview_url = 'https://image.maps.api.here.com/mia/1.6/mapview'

app_id = os.environ["HERE_APP_ID"]
app_code = os.environ["HERE_APP_CODE"]
app_payload = {'app_id': os.environ["HERE_APP_ID"], 'app_code': os.environ["HERE_APP_CODE"]}

# makes a request to the specified url with the specified app_payload
# NOTE: this will automatically generate a payload with the default app code and id
def make_request(url, payload):
    final_payload = dict(app_payload)
    final_payload.update(payload)
    return requests.get(url, params=final_payload)

def create_test_image():
    response = requests.get(mapview_url, payload)
    newFile = open("here_test.jpg", "wb")
    newFile.write(response.content)

def get_geocode_from_search(search_string):
    payload = {'searchtext': search_string.replace(' ', '+')}
    response = make_request(geocoder_url, payload)
    return response.text
