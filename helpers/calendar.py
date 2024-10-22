import os.path
import datetime
from logging import getLogger
from typing import Optional, Any

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_creds() -> Credentials:
    """
    Gets creds to the project app, that grants access to the calender.
    The file, token.json stores the access token and refresh token. credentials.json is used to get the token.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                print("Refresh token expired, a new token will have to be aquired using credentials.json")
                # We raise here since this code is usually executed in the platform the bot is ran
                # and aquiring a new token.json file is usually done in a different environment
                raise
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def get_available_calendars():
    creds = get_calendar_creds()
    print("Acquired Credentials")

    try:
        service = build("calendar", "v3", credentials=creds)

        calendar_list = service.calendarList().list().execute()

        for calendar in calendar_list["items"]:
            print(f'{calendar["id"]} - ' \
                  # This code reverses the calendar name if it is in hebrew
                  f'{calendar["summary"][::-1]}'
                  if (any("\u0590" <= c <= "\u05EA" for c in calendar["summary"]))  # Unicode range for hebrew
                  else f'{calendar["summary"]}'
            )
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        return None

def get_daily_events(calendar_id: str, day: datetime.datetime = None) -> Optional[list[dict[str, Any]]]:
    """
    Get all events from calender in a specific date

    :param calendar_id: Id of calendar to query, used by google api.
    :param day: Day to get events from. If none, uses today's date
    """
    today_base = day
    if not today_base:
        today_base = datetime.datetime.today()
    today = datetime.datetime(today_base.year, today_base.month, today_base.day, 0, 0, 0, 0)
    tomorrow = today + datetime.timedelta(days=1)

    today_iso = today.isoformat() + 'Z'
    tomorrow_iso = tomorrow.isoformat() + 'Z'

    creds = get_calendar_creds()

    try:
        service = build("calendar", "v3", credentials=creds)

        logger.info(f'Getting events for {today_iso}')
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=today_iso,
                timeMax=tomorrow_iso,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events_result.get("items", [])

    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        return None
