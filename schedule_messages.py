import time
import datetime
from typing import Any
from pathlib import Path

import toml
import schedule
from discord_webhook import DiscordWebhook

def schedule_webhook(config: dict[str, Any]):
    """
    Schedule a webhook to occur, time based on the config.toml file

    :param config: Config dictionary read from config.toml
    """
    def job():
        webhook = DiscordWebhook(url=config['url'], content=config['content'])
        if ((datetime.datetime.today().weekday() + 1) % 7) in config['days']:
            webhook.execute()
            time.sleep(5)
            webhook.delete()

    schedule.every().day.at(config['hour'], 'Israel').do(job)

def main():
    with open(Path(__file__).parent.joinpath('config.toml')) as config_file:
        config = toml.load(config_file)

    for sched_config in config['schedule']:
        schedule_webhook(sched_config)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
