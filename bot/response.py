# response.py
import requests
import random
from models import Response
from models import ResponseParams
from models import ResponseBotParams
from write_appdata import write_error_to_logfile


def mention_response(request_params, action_data, message_id):
    if action_data is None:
        action_data = "No actions to take with this mention."
    response_params = ResponseParams(
        request_params.token, request_params.group_id, 'GUIDMENTION' + message_id, action_data)
    response_bot_params = ResponseBotParams(request_params.token, request_params.bot_id, action_data, None)
    return post_bot_message(response_bot_params)


def report_response(request_params, member_nickname, message_id):
    response_params = ResponseParams(request_params.token, request_params.group_id, 'GUIDREPORT' +
                                     message_id, "REPOST REPORTED: " + member_nickname + " is the alleged reposter!")
    response_bot_params1 = ResponseBotParams(request_params.token, request_params.bot_id, "https://media1.tenor.com/images/83095f49e5559a8020890853446240c9/tenor.gif", None)
    response_bot_params2 = ResponseBotParams(request_params.token, request_params.bot_id, "REPOST REPORTED: " + member_nickname + " is the alleged reposter!", None)
    result1 = post_bot_message(response_bot_params1)
    if result1.status == 202:
        return post_bot_message(response_bot_params2)
    else:
        return result1


def post_bot_message(response_bot_params):
    bot_params = {}
    bot_params['bot_id'] = vars(response_bot_params)['bot_id']
    bot_params['text'] = vars(response_bot_params)['text']
    if response_bot_params.picture_url is not None:
        bot_params['picture_url'] = vars(response_bot_params)['picture_url']
    result = requests.post('https://api.groupme.com/v3/bots/post', params=bot_params)
    if result.status_code == 201:
        print("EVENT: POST 201 SUCCESSFUL RESPONSE")
        created_response = result.json()['response']['message']
        response = Response(201, created_response['id'], None)
        return response
    if result.status_code == 202:
        print("EVENT: POST 202 SUCCESSFUL RESPONSE")
        response = Response(202, None, bot_params['text'])
        return response
    if result.status_code == 400:
        print("ERROR: POST 400 BAD REQUEST")
        write_error_to_logfile("ERROR: POST 400 BAD REQUEST")
        return False
    if result.status_code == 401:
        print("ERROR: POST 401 UNAUTHORIZED")
        write_error_to_logfile("ERROR: POST 401 UNAUTHORIZED")
        return False
    if result.status_code == 409:
        print("ERROR: POST 409 CONFLICT")
        write_error_to_logfile("ERROR: POST 409 CONFLICT")
        return False
    else:
        print("ERROR: REQUEST EXCEPTION")
        raise requests.exceptions.RequestException
