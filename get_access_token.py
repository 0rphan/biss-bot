from os.path import exists

from helpers.calendar import get_calendar_creds, get_available_calendars

def main():
    """
    This function is used to get the token.json file. Since the authorization process requires a web browser GUI,
    if the host VM running the bot is a CLI server, the function should be called from outside, and the file
    token.json should be transferred into the VM.
    """
    if not exists('credentials.json'):
        print("File credentials.json is not present in the working directory")
        print("To get the credentials.json file, follow the guide in "
              "https://developers.google.com/calendar/api/quickstart/python")
        return

    get_calendar_creds()

    print("Lists all available calendars")

    get_available_calendars()

if __name__ == "__main__":
    main()
