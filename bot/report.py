#report.py
from response import report_response
from read_appdata import read_member_data
from write_appdata import write_report_json

def handle_report(request_params, report):
    result = None
    if report != None:
        written = write_report(report)
        if written:
            return report_response(request_params, report.report_nickname, report.message_id)
        elif not written:
            return "Report already exists and will not be written to json..."
    return result    

def write_report(report):
    return write_report_json(report, read_member_data())