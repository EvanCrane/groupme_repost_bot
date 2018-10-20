#bot.py
import time
from models import RequestParams
from read_appdata import read_appdata
from request_handler import handle_get_requests

def bot_main():
    model_objects = bot_start()
    while True:
        handle_get_requests(model_objects.get("request_params"))
        time.sleep(30)
        print("Main Loop Finished...\n")
def bot_start():
    return read_appdata()

bot_main()