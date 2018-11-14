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
    appdata["http_params"] = get_json_data(filepaths.get("http_params"))
    appdata["handler_params"] = get_json_data(filepaths.get("handler_params"))
    appdata["member_data"] = get_json_data(filepaths.get("member_data"))
    appdata["response"] = get_json_data(filepaths.get("response"))
    objects = bind_data_to_objects(appdata)
    return objects


def read_member_data():
    appdata = {}
    filepaths = define_filepaths()
    appdata["member_data"] = get_json_data(filepaths.get("member_data"))
    member_data = bind_member_to_object(appdata)
    return member_data


def get_json_data(path):
    verify_file(path)
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def bind_member_to_object(appdata):
    object = {}
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
    object["member_data"] = member_data
    return object


def bind_data_to_objects(appdata):
    objects = {}
    request_params = (appdata.get("http_params"))["request_params"]
    since_id = (appdata.get("handler_params"))["since_id"]
    request_params_obj = RequestParams(
        request_params["token"], request_params["group_id"], since_id, request_params["bot_id"])
    member_data = appdata.get("member_data")
    members = []
    for item in member_data:
        reports = []
        for rep in item["reports"]:
            report = Report(item["user_id"], rep["report_nickname"], rep["message_id"], rep["reported_by"])
            reports.append(report)
        member = Member(item["user_id"], item["nickname"], reports)
        members.append(member)
    objects["request_params"] = request_params_obj
    objects["member_data"] = member_data
    objects["response_data"] = appdata["response"]
    return objects
