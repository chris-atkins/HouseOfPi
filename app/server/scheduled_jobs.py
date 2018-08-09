#!env/bin/python

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.server.utils.ip_address_finder import IpAddressFinder
import requests

server_config = None

def report_ip_address():
    global server_config
    ip_finder = IpAddressFinder(server_config)
    ip_address = ip_finder.find_current_ip_address()

    postData = {"houseIp": 'https://' + ip_address + ":5000"}
    url = server_config.get('MY_HOUSE_URL') + '/house/ip'
    requests.post(url, json=postData, verify=False)


def init_scheduled_jobs(config):
    global server_config
    server_config = config
    seconds_between_ip_reports = int(config.get("SECONDS_BETWEEN_IP_REPORTS"))
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=report_ip_address,
        trigger=IntervalTrigger(seconds=seconds_between_ip_reports),
        id='report_ip_address',
        name="Reports the currently running application's ip address to the MyHouse server",
        replace_existing=True)

    atexit.register(lambda: scheduler.shutdown())