# bot.py
import time
from models import RequestParams
from read_appdata import read_appdata
from request_handler import request_handler
from write_appdata import log_reports


def bot_main():
    model_objects = bot_start()
    while True:
        print("EVENT: Handling requests...")
        reports = request_handler(model_objects.get("request_params"))
        if reports != None:
            log_reports(reports, model_objects.get("member_data"))
            print("EVENT: Main Loop Finished...\n")
        time.sleep(15)


def bot_start():
    return read_appdata()


bot_main()
