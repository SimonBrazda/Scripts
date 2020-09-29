#!/bin/python

# Lgs connectivity state changes

import time
import os
import sys
import subprocess
import datetime

addresses = ("www.upc.cz", "www.google.com")
log_name = "connectivity_log.txt"
log_directory = "/volume1/homes/simon/logs"  # "/volume1/homes/simon/logs/$log_name"
log_path = os.path.join(log_directory, log_name)
successful_ping = "1 packets transmitted, 1 received, 0% packet loss"
failed_ping_log = "Offline"
successful_ping_log = "Online"

def log_connection(connection_msg):
    # try:
    with open(log_path, "a") as log_file:
        time = datetime.datetime.now()
        log_file.write(time.strftime("%D %T   ") + connection_msg + "\n")
    # except FileNotFoundError as err:


def ping_addresses(addresses):
    replies = []
    for address in addresses:
        replies.append(subprocess.getoutput("ping -c 1 " + address))
    return replies
    #return [subprocess.getoutput(f"ping -c 1 {address}") for address in addresses]

def is_connected(replies):
    for reply in replies:
        if successful_ping in reply:
            return True
    return False

replies = ping_addresses(addresses)
if os.path.isfile(log_path) == False:
    log_connection(successful_ping_log) if is_connected(replies) else log_connection(failed_ping_log)
    sys.exit()

if is_connected(replies) == False and successful_ping_log in subprocess.getoutput("tail -n 1 " + log_path):
    log_connection(failed_ping_log)
    sys.exit()
elif is_connected(replies) == True and failed_ping_log in subprocess.getoutput("tail -n 1 " + log_path):
    log_connection(successful_ping_log)
