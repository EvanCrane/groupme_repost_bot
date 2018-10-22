# write_appdata.py
import json
import datetime
from filepaths import define_filepaths
from models import Member
from models import Report


def log_reports(since_id, reports, member_data, is_new_messages):
    is_report_written = False
    filepaths = define_filepaths()
    if reports is not None and member_data is not None and is_new_messages:
        member_list = add_reports(reports, member_data)
        member_dict = objects_to_dict(member_list)
        if len(member_dict) > 0:
            is_report_written = write_to_member_json(filepaths, member_dict)
            is_handler_written = write_to_handler_json(filepaths, since_id)
    elif is_new_messages:
        write_to_handler_json(filepaths, since_id)
    return write_to_logfile(filepaths, since_id, reports,
                            is_report_written, is_new_messages)


def add_reports(reports, member_data):
    member_list = []
    for report in reports:
        member_match = [
            m for m in member_data if m['user_id'] == report.user_id]
        if len(member_match) > 0:
            member_reports = member_match[0].get('reports')
            report_exists = [
                r for r in member_reports if report.message_id == r['message_id']]
            if len(report_exists) == 0:
                report_objects = []
                for item in member_reports:
                    rep = Report(member_match[0].get('user_id'), item.get(
                        'report_nickname'), item.get('message_id'), item.get('reported_by'))
                    report_objects.append(rep)
                report_objects.append(report)
                updated_member = Member(
                    member_match[0]['user_id'], member_match[0]['nickname'], report_objects)
                member_list.append(updated_member)
        else:
            new_reports = []
            new_reports.append(report)
            new_member = Member(
                report.user_id, report.report_nickname, new_reports)
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


def write_to_handler_json(filepaths, since_id):
    with open(filepaths.get("handler_params"), 'w') as outfile:
        json.dump({'since_id': since_id}, outfile)


def write_to_member_json(filepaths, member_dict):
    with open(filepaths.get("member_data"), 'w') as outfile:
        json.dump(member_dict, outfile)
    return True


def write_to_logfile(filepaths, since_id, reports, is_report_written, is_new_messages):
    now = datetime.datetime.now()
    logheader = "LOG EVENT | TIME: " + \
        str(now) + '\n' + "SINCE_ID: " + since_id
    logtype = "LOG TYPE: "
    logreportstatus = "REPORT STATUS: "
    logerror = '\n\t - ' + "ERROR: "
    logfooter = "REPORTS: "

    # New messages
    if is_new_messages:
        # New messages with reports
        if reports is not None:
            report_ids = [r.message_id for r in reports]
            logfooter += str(report_ids)

            # New messages with reports written to json
            # Outcome1
            if is_report_written:
                logtype += "newmessage_writtenreports"
                logreportstatus += "Repost report and written"
                logerror = ""

            # New messages with reports written to json BUT somehow the reports already exists.
            # Log as error
            # Outcome2
            else:
                logtype += "newmessage_writtenreports_error_existing"
                logreportstatus += "Repost report and written BUT the report(s) already exists"
                logerror = "ERROR: Report(s) reported but already exists"

            logbody = '\t - ' + logtype + '\n\t - ' + \
                logreportstatus + logerror
        # New messages but no reports (High outcome)
        # Outcome3
        else:
            logbody = "New messages but no reports"

    # No new messages (Very High outcome)
    # Outcome4
    else:
        logbody = "No new messages"

    logmessage = logheader + '\n' + logbody + '\n' + logfooter + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    return True


def write_error_to_logfile(error):
    filepaths = define_filepaths()
    now = datetime.datetime.now()
    border = "*****************************************************"
    logheader = "LOG EVENT | TIME: " + str(now)
    logbody = "ERROR | EXCEPTION THROWN"
    errormessage = str(error[0]) + '\n' + str(error[1]
                                              ) + '\n' + str(error[2].tb_frame)
    logmessage = '\n' + border + '\n' + logheader + '\n' + \
        logbody + '\n' + errormessage + '\n' + border + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    print(logmessage)
    return False
