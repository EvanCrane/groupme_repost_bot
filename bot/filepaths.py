# filepaths.py
import os.path


def define_filepaths():
    filepaths = {}
    root_path = os.path.dirname("AppData/")
    filepaths["http_params"] = root_path + "/http_params.json"
    filepaths["handler_params"] = root_path + "/handler_params.json"
    filepaths["member_data"] = root_path + "/member_data.json"
    filepaths["response"] = root_path + "/response.json"
    filepaths["logfile"] = root_path + "/logfile.md"
    return filepaths


def verify_file(file_path):
    if os.path.exists(file_path) or os.path.getsize(file_path) > 0:
        return True
    else:
        raise ValueError("AppData file missing or it is empty!")
