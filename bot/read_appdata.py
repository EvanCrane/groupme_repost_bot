# read_appdata.py
import json
import os.path
from models import RequestParams


def read_appdata():
    appdata = {}
    filepaths = define_filepaths()
    appdata["http_params"] = get_http_params(filepaths.get("http_params"))
    #appdata["user_data"] = get_user_data(filepaths.get("user_data"))
    #appdata["response"] = get_response(filepaths.get("response"))
    objects = bind_data_to_objects(appdata)
    return objects


def define_filepaths():
    filepaths = {}
    root_path = os.path.dirname("AppData/")
    filepaths["http_params"] = root_path + "/http_params.json"
    filepaths["user_data"] = root_path + "/user_data.json"
    filepaths["response"] = root_path + "/response.json"
    return filepaths


def get_http_params(path):
    verify_file(path)
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def get_user_data(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def get_response(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def verify_file(file_path):
    if os.path.exists(file_path) or os.path.getsize(file_path) > 0:
        return True
    else:
        raise ValueError("AppData file missing or it is empty!")

def bind_data_to_objects(appdata):
    objects = {}
    request_params = (appdata.get("http_params"))["request_params"]
    request_params_obj = RequestParams(request_params.get("token"), request_params.get("group_id"))
    objects["request_params"] = request_params_obj
    return objects