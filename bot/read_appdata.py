# read_appdata.py
import json
from filepaths import define_filepaths
from filepaths import verify_file
from models import RequestParams
from models import Member
from models import Report


def read_appdata():
    appdata = {}
    filepaths = define_filepaths()
    appdata["http_params"] = get_http_params(filepaths.get("http_params"))
    appdata["member_data"] = get_member_data(filepaths.get("member_data"))
    #appdata["response"] = get_response(filepaths.get("response"))
    objects = bind_data_to_objects(appdata)
    return objects


def get_http_params(path):
    verify_file(path)
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def get_member_data(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def get_response(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def bind_data_to_objects(appdata):
    objects = {}
    request_params = (appdata.get("http_params"))["request_params"]
    request_params_obj = RequestParams(
        request_params.get("token"), request_params.get("group_id"))
    member_data = appdata.get("member_data")
    members = []
    for item in member_data:
        reports = []
        for rep in item.get("reports"):
            report = Report(item.get("user_id"), rep.get(
                "report_nickname"), rep.get("message_id"), rep.get("reported_by"))
            reports.append(report)
        member = Member(item.get("user_id"), item.get("nickname"), reports)
        members.append(member)
    objects["request_params"] = request_params_obj
    objects["member_data"] = member_data
    return objects
