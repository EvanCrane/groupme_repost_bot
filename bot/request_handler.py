# request_handler.py
import sys
import os
import requests
from models import RequestParams
from models import Member
from models import Report
from mention import handle_mention
from report import handle_report


def request_handler(request_params, response_data):
    try:
        message_params = form_message_params(request_params)
        member_params = form_member_params(request_params)
        response = handle_get_requests(message_params, request_params.group_id)
        if len(response) == 0 or request_params.since_id == response[0]:
            print("EVENT: Nothing has happened in the group since id: " +
                  request_params.since_id)
            return request_params.since_id
        # Get all current members after all new messages retrieved
        current_members = get_members(member_params, request_params.group_id)
        messages_to_log = handle_messages(response[-1], request_params, current_members)
        if len(messages_to_log) > 0:
            return [response[0], messages_to_log]
        else:
            print("EVENT: New messages but no reposts reported...")
            return [response[0]]
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return (exc_type, fname, exc_tb.tb_lineno)


def form_message_params(request_params):
    message_params = {}
    if len(request_params.since_id) > 0:
        message_params['since_id'] = request_params.since_id
    message_params['token'] = request_params.token
    return message_params


def form_member_params(request_params):
    member_params = {}
    member_params['token'] = request_params.token
    return member_params


def handle_get_requests(request_params, group_id):
    response = requests.get('https://api.groupme.com/v3/groups/'
                            + group_id + '/messages',
                            params=request_params)
    if response.status_code == 200:
        response_messages = response.json()['response']['messages']
        return [response_messages[0]['id'], response_messages]
    if response.status_code == 304:
        return []
    else:
        raise requests.exceptions.RequestException


def handle_messages(response_messages, request_params, current_members):
    messages_to_log = []
    for message in (list(reversed(response_messages))):
        if message['text'] != None:
            if '@REPOST' in message['text'].upper():
                print("EVENT: A MENTION HAS BEEN DETECTED...")
                mention = {'message_id': message['id'], 'mentioned_by': message['user_id'],
                           'action_text': message['text'].upper().split('@REPOST')[1].strip(),
                           'full_message': message['text']}
                # Handle mention
                result = handle_mention(request_params, mention)
                messages_to_log.append(("MENTION", result))
            elif 'REPOST' in message['text'].upper() and '@' in message['text'].upper():
                print("EVENT: A REPOST HAS BEEN REPORTED...")
                # @nickname is the name that is picked up from the message text
                nickname = message['text'].split('@')[1].strip()
                prereport = {'@nickname': nickname,
                             'message_id': message['id'], 'reported_by': message['user_id']}
                # Handle repost
                report = match_member_nickname(current_members, prereport)
                if report is None:
                    # No matches
                    print("EVENT: Report did not contain a matching group member...")
                    messages_to_log.append(("FALSE REPOST", prereport))
                    break
                response = handle_report(request_params, report)
                messages_to_log.append(("REPOST", (report, response)))
    return messages_to_log


def get_members(member_params, group_id):
    response = requests.get(
        'https://api.groupme.com/v3/groups/' + group_id, params=member_params)
    if response.status_code == 200:
        response_members = response.json()['response']['members']
        return response_members
    else:
        raise requests.exceptions.RequestException


def match_member_nicknames(reported_messages, members):
    reports = []
    for member in members:
        for message in reported_messages:
            if member['nickname'] in message.get('@nickname'):
                report = Report(member['user_id'], member['nickname'], message.get(
                    'message_id'), message.get('reported_by'))
                reports.append(report)
    return reports


def match_member_nickname(members, prereport):
    #matches = [m for m in members if m['nickname'] in prereport['@nickname']]
    report = None
    for member in members:
        if member['nickname'] in prereport['@nickname']:
            report = Report(member['user_id'], member['nickname'], prereport['message_id'],
                            prereport['reported_by'])
    return report
