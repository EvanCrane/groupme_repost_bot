# models.py


class RequestParams(object):
    def __init__(self, token, group_id, since_id, bot_id):
        self.token = token
        self.group_id = group_id
        self.since_id = since_id
        self.bot_id = bot_id


class ResponseParams(object):
    def __init__(self, token, group_id, source_guid, text):
        self.token = token
        self.group_id = group_id
        self.source_guid = source_guid
        self.text = text


class ResponseBotParams(object):
    def __init__(self, token, bot_id, text, picture_url):
        self.token = token
        self.bot_id = bot_id
        self.text = text
        self.picture_url = picture_url


class Member(object):
    def __init__(self, user_id, nickname, reports):
        self.user_id = user_id
        self.nickname = nickname
        self.reports = reports


class Report(object):
    def __init__(self, user_id, report_nickname, message_id, reported_by):
        self.user_id = user_id
        self.report_nickname = report_nickname
        self.message_id = message_id
        self.reported_by = reported_by


class Mention(object):
    def __init__(self, message, message_id, mentioned_by, full_message):
        self.message = message
        self.message_id = message_id
        self.mentioned_by = mentioned_by
        self.full_message = full_message


class Action(object):
    def __init__(self, action_cmd, action_result, mention):
        self.action_cmd = action_cmd
        self.action_result = action_result
        self.mention = mention


class Response(object):
    def __init__(self, status, message_id, text):
        self.status = status
        self.message_id = message_id
        self.text = text
