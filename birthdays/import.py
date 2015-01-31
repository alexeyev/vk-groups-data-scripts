# -*- coding:utf-8 -*-

import sys
import json
from urllib2 import *

"""
Call example:
$ python 2 import.py
"""

NO_BDATE = "no_bdate"

my_id = sys.argv[1]
results_file_path = sys.argv[1] + ".csv"

print "Fetching birthdays for id", my_id, "; results to be stored in", results_file_path

url_pattern = "https://api.vk.com/method/friends.get?fields=city,bdate&user_id="

def fix_bdate(bd):
    if bd == NO_BDATE:
        return NO_BDATE
    else:
        splitted = bd.split(".")
        if len(splitted) == 3:
            return bd
        else:
            return bd + ".1648"

def json_to_line(o):
    try:
        bdate = str(o['bdate'])
    except Exception,e:
        bdate = NO_BDATE
    return fix_bdate(bdate) + "\t" + "\t".join([str(o['uid']), str(o['user_id']), o['first_name'], o['last_name']]) + "\n"

with open(results_file_path, "w+") as wfile:
    raw_response = urlopen(url_pattern + my_id).read()
    json_data = json.loads(raw_response.strip())
    for record in json_data['response']:
        print json_to_line(record),
        wfile.write(json_to_line(record).encode('UTF-8'))