import sys
import json
from urllib2 import *

"""
Call example:
$ python

"""


my_id = sys.argv[1]

print "Fetching birthdays for id", my_id

url_pattern = "https://api.vk.com/method/friends.get?fields=city,bdate&user_id="
headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5)', 'Content-type' : 'text/html; charset=UTF8'}

def json_to_line(o):
    try:
        bdate = str(o['bdate'])
    except Exception,e:
        bdate = "no_bdate"    
    #todo: str(o['hidden']),str(o['city'])
    return bdate + "\t" + "\t".join([str(o['uid']), str(o['user_id']), o['first_name'], o['last_name']]) + "\n"

with open(sys.argv[2], "w+") as wfile:
    raw_response = urlopen(url_pattern + my_id).read()
    json_data = json.loads(raw_response.strip())
    #print json_data
    #print json_data['response']
    for record in json_data['response']:
        print json_to_line(record)
        wfile.write(json_to_line(record).encode('UTF-8'))

# my calendar: qdm2cma6nmsucvvsftopjlru6c@group.calendar.google.com
