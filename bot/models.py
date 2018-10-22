# models.py


class RequestParams(object):
    def __init__(self, token, group_id, since_id):
        self.token = token
        self.group_id = group_id
        self.since_id = since_id

class Member(object):
    def __init__(self, user_id, nickname, reports):
        self.user_id = user_id
        self.nickname = nickname
        self.reports = reports


class Report(object):
    def __init__(self, user_id, report_nickname ,message_id, reported_by):
        self.user_id = user_id
        self.report_nickname = report_nickname
        self.message_id = message_id
        self.reported_by = reported_by
