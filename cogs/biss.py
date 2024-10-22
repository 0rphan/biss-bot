import json
import datetime
from pathlib import Path

import aiohttp
import discord

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, calendar, discord_tools


class Biss(commands.Cog, name="biss"):

    DATE_FORMAT = '%d-%m-%Y'
    TIME_FORMAT = '%H:%M'
    CALENDAR_DELIMITER = ' | '

    def __init__(self, bot):
        self.bot = bot
        with open(Path(__file__).parent.parent.joinpath('config.json')) as config_file:
            self.config = json.load(config_file)

    @commands.hybrid_command(
        name="info",
        description="This command give command about a student",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def info(self, context: Context):
        """
        This command give command about a student

        :param context: The application command context.
        """

        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(
                description="Hanich Hanichi\nהערות משמעות: 69", color=0xD75BF4)
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="looz",
        description="This command gives you today's looz. Can also take a date in the format dd-mm-yyyy as input.",
    )
    @checks.not_blacklisted()
    async def looz(self, context: Context, date: str = None):
        """"
        This command gives you today's looz
        Can also take a date in the format dd-mm-yyyy as input.

        :param context: The application command context.
        """
        if not date:
            date = datetime.datetime.today().strftime(self.DATE_FORMAT)

        events = calendar.get_daily_events(self.config['calendar_id'], datetime.datetime.strptime(date, self.DATE_FORMAT))
        if events is None:
            return

        if not events:
            async with aiohttp.ClientSession() as session:
                embed = discord.Embed(
                    description='אין לו"ז להיום! חבורת חפשנים!', color=0xD75BF4)
                await context.send(embed=embed)
            return

        embed = discord.Embed(title='לו"ז להיום', color=0xD75BF4)

        for index, event in enumerate(events):
            if index and index % 25 == 0:  # Max amount of fields in a single embed
                async with aiohttp.ClientSession() as session:
                    await context.send(embed=embed)
                embed = discord.Embed(color=0xD75BF4)

            start = None
            end = None
            is_all_day = bool(event["start"].get("dateTime", False))
            if not is_all_day:
                start = event["start"]["date"]
                if datetime.datetime.strptime(date, self.DATE_FORMAT) < datetime.datetime.strptime(start, '%Y-%m-%d'):
                    continue
                end = 'כל היום'
            else:
                start_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                end_time = datetime.datetime.fromisoformat(event["end"]["dateTime"])
                start_hour = start_time.strftime(self.TIME_FORMAT)
                end_hour = end_time.strftime(self.TIME_FORMAT)
                start = start_hour
                end = end_hour
            embed.add_field(name='',
                            value=f'{start} - {end} : {event["summary"]}',
                            inline=False)

        async with aiohttp.ClientSession() as session:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="madrat",
        description="This command gives you today's madrat",
    )
    async def madrat(self, context: Context):
        """
        This command gives you today's and tomorrow's madrat

        :param context: The application command context.
        """
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)

        today_events = calendar.get_daily_events(self.config['calendar_id'], today)
        tomorrow_events = calendar.get_daily_events(self.config['calendar_id'], tomorrow)

        found_today, found_tomorrow = False, False

        for event in today_events:
            event_type, *data = str(event["summary"]).split(self.CALENDAR_DELIMITER, 2)
            if not event_type == 'מדרת':
                continue
            found_today = True
            madrat = discord_tools.match_channel_member(context, data[0])
            await context.send('@everyone ' + 'המדר"ת להיום - ' + f'<@{madrat.id}>')

        for event in tomorrow_events:
            event_type, *data = str(event["summary"]).split(self.CALENDAR_DELIMITER, 2)
            if not event_type == 'מדרת':
                continue
            found_tomorrow = True
            madrat = discord_tools.match_channel_member(context, data[0])
            await context.send('@everyone ' + 'המדר"ת למחר - ' + f'<@{madrat.id}>')
        if not all([found_today, found_tomorrow]):
            await context.send('לא נמצא מדרת - ' +
                               ('היום' if not found_today else '') +
                               (' ו' if not (found_today and found_tomorrow) else '') +
                               ('מחר' if not found_tomorrow else '')
                              )

    @commands.hybrid_command(
        name="nikayon",
        description="This command gives you today's 'toraney nikayon'",
    )
    async def nikayon(self, context: Context):
        """
        This command gives you today's 'toraney nikayon'

        :param context: The application command context.
        """
        today = datetime.datetime.today()

        today_events = calendar.get_daily_events(self.config['calendar_id'], today)

        found_today = False
        for event in today_events:
            event_type, *data = str(event["summary"]).split(self.CALENDAR_DELIMITER, 2)
            if not event_type == 'תורני ניקיון ופריסה':
                continue
            found_today = True
            toran_1 = discord_tools.match_channel_member(context, data[0])
            toran_2 = discord_tools.match_channel_member(context, data[1])
            if toran_1 is None or toran_2 is None:
                await context.send('השם של אחד התורנים בקאלנדר לא נמצא בשרת! ככל הנראה מדובר בשגיאת כתיב.')
                return

            await context.send('@everyone ' + 'תורני הניקיון והפריסה להיום - ' + f'<@{toran_1.id}> <@{toran_2.id}>')

        if not found_today:
            await context.send('לא נמצאו תורני ניקיון להיום')

    @commands.hybrid_command(
        name="sahi",
        description="This command gives you today's and tomorrow's 'sahi'",
    )
    @checks.not_blacklisted()
    async def sahi(self, context: Context):
        """
        This command gives you today's and tomorrow's sahi

        :param context: The application command context.
        """
        with open("database/sahi.csv", 'r', encoding="utf8") as file:
            csvreader = csv.reader(file)
            tomorrow = (datetime.datetime.now() +
                        datetime.timedelta(days=1)).strftime("%m/%d/%y")
            today = (datetime.datetime.now()).strftime("%m/%d/%y")
            pretty_tomorrow = (datetime.datetime.now() +
                           datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            pretty_today = (datetime.datetime.now()).strftime("%d/%m/%Y")

            desc = f""
            for row in csvreader:
                if row[0] == today:
                    desc += f"[{pretty_today}] מעביר האקטואליה היומית היום - {row[1]}\n"
                if row[0] == tomorrow:
                    desc += f"[{pretty_tomorrow}] מעביר האקטואליה היומית מחר - {row[1]}\n"

            if desc:
                embed = discord.Embed(
                    title="אקטואליה יומית",
                    description=desc,
                    color=0xD75BF4)
                await context.send(embed=embed)
                return

        embed = discord.Embed(description="אין 'אקטואליה יומית' היום או מחר", color=0xE02B2B)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Biss(bot))
