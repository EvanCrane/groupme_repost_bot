# read_appdata.py
import json
from filepaths import define_filepaths
from filepaths import verify_file
from models import RequestParams


def read_appdata():
    appdata = {}
    filepaths = define_filepaths()
    appdata["http_params"] = get_http_params(filepaths.get("http_params"))
    #appdata["member_data"] = get_member_data(filepaths.get("member_data"))
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
    objects["request_params"] = request_params_obj
    return objects
