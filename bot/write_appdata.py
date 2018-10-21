#write_appdata.py
import json
import datetime
from filepaths import define_filepaths
from models import Member
from models import Report

def log_reports(reports, member_data):
    is_report_written = False
    filepaths = define_filepaths()
    member_list = add_reports(reports, member_data)
    member_dict = objects_to_dict(member_list)
    if len(member_dict) > 0:
        is_report_written = write_to_json(filepaths, member_dict)
    write_to_logfile(filepaths, reports, is_report_written)
    
    
def add_reports(reports, member_data):
    member_list = []
    for report in reports:
        member_match = [m for m in member_data if m['user_id'] == report.user_id]
        if len(member_match) > 0:
            member_reports = member_match[0].get('reports')
            report_exists = [r for r in member_reports if report.message_id == r['message_id']]
            if len(report_exists) == 0:
                existing_reports = member_match[0].get('reports')
                report_objects = []
                for item in existing_reports:
                    rep = Report(member_match[0].get('user_id'), item.get('report_nickname'), item.get('message_id'), item.get('reported_by'))
                    report_objects.append(rep)
                report_objects.append(report)
                updated_member = Member(member_match[0]['user_id'], member_match[0]['nickname'], report_objects)
                member_list.append(updated_member)
        else:
            new_reports = []
            new_reports.append(report)
            new_member = Member(report.user_id, report.report_nickname, new_reports)
            member_exists = False
            for member in member_list:
                if member.user_id == new_member.user_id:
                    member.reports.extend(new_member.reports)
                    member_exists = True
            if member_exists is False:
                member_list.append(new_member)
    return member_list


def objects_to_dict(member_list):
    member_dict = []
    for member in member_list:
        sub_dict = {}
        sub_dict["user_id"] = member.user_id
        sub_dict["nickname"] = member.nickname
        reports = []
        for report in member.reports:
            report_dict = {}
            report_dict["message_id"] = report.message_id
            report_dict["report_nickname"] = report.report_nickname
            report_dict["reported_by"] = report.reported_by
            reports.append(report_dict)
        sub_dict["reports"] = reports
        member_dict.append(sub_dict)
    return member_dict
    

def write_to_json(filepaths, member_dict):
    with open(filepaths.get("member_data"), 'w') as outfile:
        json.dump(member_dict, outfile)
    return True

def write_to_logfile(filepaths, reports, is_report_written):
    now = datetime.datetime.now()
    report_ids = [r.message_id for r in reports]
    logheader = "LOG EVENT | TIME: " + str(now)
    logfooter = "REPORTS: " + str(report_ids)
    if is_report_written:
        logbody = "REPOST STATUS: Repost report and written..."
    elif is_report_written is False and reports is not None:
        logbody = "REPOST STATUS: Repost reported but it already exists..."
    else:
        logbody = "REPOST STATUS: Nothing to report in this loop..."
        logfooter = ""
    logmessage = logheader + "\n" + logbody + "\n" + logfooter + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    print(logbody)