# bot.py
import time
from models import RequestParams
from read_appdata import read_appdata
from request_handler import request_handler
from write_appdata import log_reports
from write_appdata import write_error_to_logfile


def bot_main():
    while True:
        model_objects = bot_start()
        print("EVENT: Handling requests...")
        reports = request_handler(model_objects.get("request_params"))
        if isinstance(reports, list):
            # New messages and new reports
            if len(reports) > 1:
                log_reports(reports[0], reports[-1],
                            model_objects.get("member_data"), True)
            # New messages but no new reports
            elif len(reports) == 1:
                log_reports(reports[0], None, None, True)
        # No new messages
        elif isinstance(reports, str):
            log_reports(reports, None, None, False)
        # Error thrown
        else:
            print("BOT LOOP ENDED BY ERROR...")
            return write_error_to_logfile(reports)
        print("EVENT: Main Loop Finished...\n")
        time.sleep(15)
    print("BOT LOOP ENDED BY ERROR...")


def bot_start():
    return read_appdata()


bot_main()
