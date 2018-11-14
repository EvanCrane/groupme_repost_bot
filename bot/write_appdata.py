# write_appdata.py
import json
import datetime
from filepaths import define_filepaths
from models import Member
from models import Report
from models import Mention
from models import Action
from models import Response


def write_report_json(report, member_data):
    filepaths = define_filepaths()
    member = add_report(report, member_data)
    #reports['reports'] = member.reports
    #updated_member = Member(member.user_id, member.nickname, reports)
    member_dict = object_to_dict(member)
    members = []
    members.append(member_dict)
    if len(member_dict) > 0:
        is_report_written = write_to_member_json(filepaths, members)
        return True
    else:
        print("Report already exists and will not be written to json...")
        return False


def add_report(report, member_data):
    #member_match = [(k,m) for k,m in member_data.items() if m['user_id'] == report.user_id]
    member_match = []
    for k, m in member_data.items():
        for x in m:
            if x['user_id'] == report.user_id:
                member_match.append(x)
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
            return updated_member
    else:
        new_reports = []
        new_reports.append(report)
        new_member = Member(
            report.user_id, report.report_nickname, new_reports)
        return new_member


def log_messages(since_id, messages, is_new_messages):
    is_report_written = False
    filepaths = define_filepaths()
    write_to_handler_json(filepaths, since_id)
    return write_to_logfile(filepaths, since_id, messages, is_new_messages)


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


def object_to_dict(member):
    member_dict = {}
    member_dict["user_id"] = member.user_id
    member_dict["nickname"] = member.nickname
    reports = []
    for report in member.reports:
        report_dict = {}
        report_dict["message_id"] = report.message_id
        report_dict["report_nickname"] = report.report_nickname
        report_dict["reported_by"] = report.reported_by
        reports.append(report_dict)
    member_dict["reports"] = reports
    return member_dict


def write_to_handler_json(filepaths, since_id):
    with open(filepaths.get("handler_params"), 'w') as outfile:
        json.dump({'since_id': since_id}, outfile)
    return True


def write_to_member_json(filepaths, member_dict):
    with open(filepaths.get("member_data"), 'w') as outfile:
        json.dump(member_dict, outfile)
    return True


def write_to_logfile(filepaths, since_id, messages, is_new_messages):
    now = datetime.datetime.now()
    logheader = "LOG EVENT | TIME: " + \
        str(now) + '\n' + "SINCE_ID: " + since_id
    logtype = "LOG TYPE: "
    logreportstatus = "MESSAGE STATUS: "
    logerror = ""
    logreports = "REPORTS: "
    logmentions = "MENTIONS: "
    logresponses = "RESPONSES: "
    logfooter = ""
    fulllog = "\n"
    # New messages
    if is_new_messages:
        # New messages with reports or mentions
        if messages is not None:
            for message in messages:
                if message[0] == "MENTION":
                    mention = message[1][0]
                    action = message[1][1]
                    response = message[1][2]
                    if not response:
                        logerror = "ERROR: RESPONSE ERROR"
                    logtype += "MENTION; "
                    logmentions += str("id:" + mention.message_id +
                                       " actioncmd: " + action.action_cmd + "; ")
                    if response.message_id is None:
                        logresponses += "response text: " + response.text + "; "
                    else:
                        logresponses += "response id: " + response.message_id + "; "
                elif message[0] == "REPOST":
                    report = message[1][0]
                    response = message[1][1]
                    if not response:
                        logerror = "ERROR: RESPONSE ERROR"
                    logtype += "REPOST; "
                    if response.message_id is None:
                        logresponses += "response text: " + response.text + "; "
                    else:
                        logresponses += "response id: " + response.message_id + "; "
                    logreports += "Message_id: " + report.message_id + "; "
                elif message[0] == "FALSE REPOST":
                    logtype += "FALSE REPOST; "
                    logerror += "ERROR: REPOST WAS REPORTED BUT IT WAS ALREADY LOGGED. ID: " + \
                        message[1].message_id + "; "
            logdata = logreports + '\n' + logmentions + '\n' + logresponses
            logbody = '\t - ' + logtype + '\n\t - ' + \
                logreportstatus + logerror + '\n' + logdata + '\n'
        # New messages but no reports (High outcome)
        # Outcome3
        else:
            logbody = "New messages but no reports"

    # No new messages (Very High outcome)
    # Outcome4
    else:
        logbody = "No new messages"
        logfooter = ""

    logmessage = logheader + '\n' + logbody + '\n' + logfooter + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    print(logmessage)
    return True


def write_mention_to_logfile(mention):
    filepaths = define_filepaths()
    now = datetime.datetime.now()
    logheader = "LOG EVENT | TIME: " + str(now)
    logtype = "LOG TYPE: MENTION"
    logbody = ""
    logfooter = ""
    logmessage = logheader + '\n' + logbody + '\n' + logfooter + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    return True


def write_error_to_logfile(error):
    filepaths = define_filepaths()
    now = datetime.datetime.now()
    border = "*****************************************************"
    logheader = "LOG EVENT | TIME: " + str(now)
    # is exception
    if isinstance(error, tuple):
        logbody = "ERROR | EXCEPTION THROWN"
        errormessage = str(error[0]) + '\n' + \
            str(error[1]) + " Line: " + str(error[2])
    # non critical error
    else:
        logbody = "ERROR | NON CRITICAL ERROR"
        errormessage = error
    logmessage = '\n' + border + '\n' + logheader + '\n' + \
        logbody + '\n' + errormessage + '\n' + border + '\n'
    with open(filepaths.get("logfile"), 'a') as f:
        f.write(logmessage)
    print(logmessage)
    return False
