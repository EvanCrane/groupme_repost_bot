# request_handler.py
import requests
from models import RequestParams


def handle_get_requests(params):
    request_params = {'token': params.token}
    response_messages = requests.get('https://api.groupme.com/v3/groups/'
                                     + params.group_id + '/messages',
                                     params=request_params).json()['response']['messages']
    for item in response_messages:
        print(item['text'])