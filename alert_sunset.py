import datetime
from time import sleep

from astral.sun import sun
from astral import LocationInfo
from schedule import Job as _Job
from discord_webhook import DiscordWebhook
from schedule import Scheduler as _Scheduler

WEBHOOK_URL = r""
EXECUTE_ON_DAYS = [0, 1, 2, 3, 4]
CITY = LocationInfo("Jerusalem", "Israel", "Israel", 31.771959, 35.217018)

def job_alert_sunset():
    webhook = DiscordWebhook(url=WEBHOOK_URL, content="@everyone Sundown is in 10 minutes!")
    if (datetime.datetime.today().weekday() + 1) % 7 in EXECUTE_ON_DAYS:
        webhook.execute()


class Job(_Job):
    city = CITY
    last_sunrise = None
    last_sunset = None

    last_sunrise_offset = 0
    last_sunset_offset = 0

    def __init__(self, interval, scheduler):
        super().__init__(interval, scheduler)

    def at_sunrise(self, minute_offset: int):
        s = sun(self.city.observer, date=self.next_run)
        self.last_sunrise = s["sunrise"]
        self.last_sunrise_offset = minute_offset
        return self.at((self.last_sunrise - datetime.timedelta(minutes=minute_offset)).strftime("%H:%M:%S"))

    def at_sunset(self, minute_offset: int):
        s = sun(self.city.observer, date=self.next_run)
        self.last_sunset = s["sunset"]
        self.last_sunset_offset = minute_offset
        return self.at((self.last_sunset - datetime.timedelta(minutes=minute_offset)).strftime("%H:%M:%S"))

    def rescedule_astro(self):

        if self.last_sunset:
            self.at_sunset(self.last_sunrise_offset)

        if self.last_sunrise:
            self.at_sunrise(self.last_sunset_offset)

    def _schedule_next_run(self):
        super()._schedule_next_run()
        self.rescedule_astro()


class Scheduler(_Scheduler):

    def every(self, interval=1):
        """ 
        Schedule a new periodic job.
        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`Job <Job>`
        """
        job = Job(interval, self)
        return job


def main():
    schedule = Scheduler()
    schedule.every().day.at_sunset(-10).do(job_alert_sunset)

    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    main()
