from __future__ import print_function

import datetime
import os.path
import json
from time import strptime
from tokenize import String
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events.readonly']


@dataclass
class CalendarShiftEvent:
    summary: str
    location: str
    description: str
    month: str
    day: str
    year: str
    start: str
    end: str

    def __post_init__(self):
        if self.summary is None:
            self.summary = 'Something is going on'
        if self.location is None:
            self.location = 'Centre St-Antoine'


def main():
    events = JsonParser()
    for event in events:
        event = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': event.year + '-0' + event.month + '-' + event.day + 'T' + event.start + ':00-04:00'
            },
            'end': {
                'dateTime': event.year + '-0' + event.month + '-' + event.day + 'T' + event.end + ':00-04:00',
            },

            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 19 * 60},
                    {'method': 'popup', 'minutes': 19 * 60},
                    {'method': 'popup', 'minutes': 5 * 60},
                    {'method': 'popup', 'minutes': 6 * 60},
                    {'method': 'popup', 'minutes': 7 * 60},

                ],
            },
        }
        print(event)
        creds = None
        dev_key = "AIzaSyCc9G8vY0gS-D1lSJyea_dgEbINFEnKB_w"
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_874235512497-l3roq82q8ihrqcfp39k1un8ghvhcr0a9.apps.googleusercontent.com.json',
                    SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds, developerKey=dev_key)
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)


def JsonParser():
    global day, start, poste, end, month, tomorrowCalendarEvent, todayCalendarEvent,  after_tomorrowCalendarEvent
    f = open(r"C:\Users\ismae\IdeaProjects\ColorfulApi\src\main\resources\static\file.json")
    holder = json.loads(f.read())
    today = date.today()
    tomorrow = today + datetime.timedelta(days=1)
    after_tomorrow = today + datetime.timedelta(days=2)
    d1 = today.strftime("%d")
    d2 = tomorrow.strftime("%d")
    d3 = after_tomorrow.strftime("%d")

    for x in holder:
        if x["date"][0:2] == d1 :
            day1 = x["date"][0:2]
            poste1 =  "Tache" + " " + x["job"][7:(len(x["job"]))]
            start1 = x["hours"][0:5]
            end1 = x["hours"][8:13]
            month1 = str(strptime(x["date"][3:6], '%b').tm_mon)
            todayCalendarEvent = CalendarShiftEvent(poste1, "Centre St-Antoine", "", month1, day1, "2022", start1, end1)
            print(day1, poste1, start1)
        if x["date"][0:2] == d2:
            day2 = x["date"][0:2]
            poste2 = x["job"]
            start2 = x["hours"][0:5]
            end2 = x["hours"][8:13]
            month2 = str(strptime(x["date"][3:6], '%b').tm_mon)
            tomorrowCalendarEvent = CalendarShiftEvent(poste2, "Centre St-Antoine", "", month2, day2, "2022", start2,
                                                       end2)
            print(day2, poste2, start2)
        if x["date"][0:2] == d3:
            day3 = x["date"][0:2]
            poste3 = "Tache"+x["job"][8:(len(x["job"]))]
            start3 = x["hours"][0:5]
            end3 = x["hours"][8:13]
            month3 = str(strptime(x["date"][3:6], '%b').tm_mon)
            print(day3, poste3, start3)
            after_tomorrowCalendarEvent = CalendarShiftEvent(poste3, "Centre St-Antoine", "", month3, day3, "2022",
                                                             start3, end3)
            break

    calendarShiftEvents = [
        todayCalendarEvent,
        tomorrowCalendarEvent,
        after_tomorrowCalendarEvent
    ]
    return calendarShiftEvents


def reader():
    f = open(r"C:\Users\ismae\IdeaProjects\ColorfulApi\src\main\resources\static\file.json")
    f.read()
    print(f.read())


def Ada() :
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
    driver.get("https://virtuo.ciussscn.rtss.qc.ca/portals/home/app/login")
    print(driver.title)

    driver.quit()
if __name__ == '__main__':
    Ada()

