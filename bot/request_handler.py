# request_handler.py
import requests
from models import RequestParams
from models import Member
from models import Report


def request_handler(params):
    # TODO add since message parameter
    request_params = {'token': params.token}
    response_messages = handle_get_requests(request_params, params.group_id)
    reported_messages = handle_messages(response_messages)
    if len(reported_messages) > 0:
        members = get_members(request_params, params.group_id)
        reports = match_member_nickname(reported_messages, members)
        return reports
    else:
        print("EVENT: No reposts reported...")
        return None


def handle_get_requests(request_params, group_id):
    response_messages = requests.get('https://api.groupme.com/v3/groups/'
                                     + group_id + '/messages',
                                     params=request_params).json()['response']['messages']
    return response_messages


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


def get_members(request_params, group_id):
    response_members = requests.get('https://api.groupme.com/v3/groups/'
                                    + group_id,
                                    params=request_params).json()['response']['members']
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
