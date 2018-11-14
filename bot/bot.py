# bot.py
import time
from models import RequestParams
from read_appdata import read_appdata
from request_handler import request_handler
from write_appdata import log_messages
from write_appdata import write_error_to_logfile


def bot_main():
    while True:
        model_objects = bot_start()
        print("EVENT: Handling requests...")
        log_stack = request_handler(model_objects.get(
            "request_params"), model_objects.get("response_data"))
        if isinstance(log_stack, list):
            if len(log_stack) > 1:
                # New messages and new reports
                log_messages(log_stack[0], log_stack[-1], True)
            # New messages but no new reports
            elif len(log_stack) == 1:
                log_messages(log_stack[0], None, True)
        # No new messages
        elif isinstance(log_stack, str):
            log_messages(log_stack, None, False)
        # Error thrown
        else:
            print("BOT LOOP ENDED BY ERROR...")
            return write_error_to_logfile(log_stack)
        print("EVENT: Main Loop Finished...\n")
        time.sleep(300)
    print("BOT LOOP ENDED BY ERROR...")


def bot_start():
    return read_appdata()


bot_main()
