# -*- coding:utf-8 -*-

import sys

import httplib2
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from credentials import *
from apiclient.discovery import build


"""
 Usage:

 $ python export.py <CSV file> <timezone from IANA TZD>

 e.g.
 $ python export.py cool_guys_birthdays.csv Europe/Moscow

 IANA TZD = IANA Time Zone Database, see
 http://en.wikipedia.org/wiki/Category:Tz_database

"""


def handle_bdate(token):
    spl = token.split(".")
    if len(spl) != 3:
        raise Exception("Wrong date format")
    else:
        day = spl[2] + "-" + spl[1] + "-" + spl[0]
        # todo: better date handling
        return day + "T00:00:00.000", day + "T23:59:00.000"

if __name__ == '__main__':

    FLOW = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='calendar/v3')

    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    # Visit the Google Developers Console
    # to get a developerKey for your own application.
    service = build(serviceName='calendar', version='v3', http=http, developerKey=developerKey)

    with open(sys.argv[1], "r+") as input_csv_file:

        if len(sys.argv) > 2:
            tz = sys.argv[2]
        else:
            tz = 'Europe/Moscow'

        for line in input_csv_file:
            try:
                spltd = line.strip().split("\t")
                start, end = handle_bdate(spltd[0])
                name = spltd[3] + " " + spltd[4]
                event = {
                    'summary': 'День рождения: ' + name,
                    'start': {
                        'dateTime': start,
                        'timeZone': tz
                    },
                    'end': {
                        'dateTime': end,
                        'timeZone': tz
                    },
                    'recurrence': [
                        "RRULE:FREQ=YEARLY;UNTIL=20900701T160000Z"
                    ]
                }
                print "Pushing ", name + "..."
                created_event = service.events().insert(calendarId=calendarId, body=event).execute()
                print "Resource id:", created_event['id']
            except Exception, e:
                print "Skipping line: {", line, "} message:",  e