# request_handler.py
import sys
import requests
from models import RequestParams
from models import Member
from models import Report


def request_handler(request_params):
    try:
        message_params = form_message_params(request_params)
        member_params = form_member_params(request_params)
        response = handle_get_requests(message_params, request_params.group_id)
        if request_params.since_id == response[0]:
            print("EVENT: Nothing has happened in the group since id: " +
                  request_params.since_id)
            return request_params.since_id
        reported_messages = handle_messages(response[-1])
        if len(reported_messages) > 0:
            members = get_members(member_params, request_params.group_id)
            reports = match_member_nickname(reported_messages, members)
            print("EVENT: New messages with reports...")
            return [response[0], reports]
        else:
            print("EVENT: New messages but no reposts reported...")
            return [response[0]]
    except:
        return sys.exc_info()


def form_message_params(request_params):
    message_params = {}
    message_params['token'] = request_params.token
    if len(request_params.since_id) > 0:
        message_params['since_id'] = request_params.since_id
    return message_params


def form_member_params(request_params):
    member_params = {}
    member_params['token'] = request_params.token
    return member_params


def handle_get_requests(request_params, group_id):
    response_messages = requests.get('https://api.groupme.com/v3/groups/'
                                     + group_id + '/messages',
                                     params=request_params).json()['response']['messages']
    return [response_messages[0]['id'], response_messages]


def handle_messages(response_messages):
    reported_messages = []
    for message in response_messages:
        if message['text'] != None:
            if 'REPOST' in message['text'].upper() and '@' in message['text'].upper():
                print("EVENT: A REPOST HAS BEEN REPORTED...")
                nickname = message['text'].split('@')[1].strip()
                report = {'@nickname': nickname,
                          'message_id': message['id'], 'reported_by': message['user_id']}
                reported_messages.append(report)
    return reported_messages


def get_members(member_params, group_id):
    response_members = requests.get('https://api.groupme.com/v3/groups/'
                                    + group_id,
                                    params=member_params).json()['response']['members']
    return response_members


def match_member_nickname(reported_messages, members):
    reports = []
    for member in members:
        for message in reported_messages:
            if message.get('@nickname') == member['nickname']:
                report = Report(member['user_id'], member['nickname'], message.get(
                    'message_id'), message.get('reported_by'))
                reports.append(report)
    return reports
