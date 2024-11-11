import toml
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
        with open(Path(__file__).parent.parent.joinpath('config.toml')) as config_file:
            self.config = toml.load(config_file)

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

    async def looz_generic(self, context: Context, date: datetime.datetime, calendar_id: str, calendar_name: str, notify_empty: bool):

        if not calendar_id:
            return

        events = calendar.get_daily_events(calendar_id, date)
        if events is None:
            return

        embed = discord.Embed(title=f'לו"ז - {calendar_name}', color=0xD75BF4)

        if not events:
            if notify_empty:
                async with aiohttp.ClientSession() as session:
                    embed.description = 'אין לו"ז להיום! חבורת חפשנים!'
                    await context.send(embed=embed)
            return

        embed = discord.Embed(title=f'לו"ז - {calendar_name}', color=0xD75BF4)

        for index, event in enumerate(events):
            if index and index % 25 == 0:  # Max amount of fields in a single embed
                async with aiohttp.ClientSession() as session:
                    await context.send(embed=embed)
                embed = discord.Embed(color=0xD75BF4)

            start = None
            end = None
            is_all_day = not bool(event["start"].get("dateTime", False))
            if is_all_day:
                start = event["start"]["date"]
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
        name="looz",
        description="This command gives you today's looz. Can also take a date in the format dd-mm-yyyy as input.",
    )
    @checks.not_blacklisted()
    async def looz(self, context: Context, day_offset: str = "0"):
        """"
        This command gives you today's looz
        Can also take a date in the format dd-mm-yyyy as input.

        :param context: The application command context.
        """
        today = datetime.datetime.today()
        today = today + datetime.timedelta(days=int(day_offset))
        date = datetime.datetime(year=today.year, month=today.month, day=today.day)

        await self.looz_generic(context,
                                date,
                                self.config['calendar']['segel_main_id'],
                                'סגל כללי',
                                True)
        await self.looz_generic(context,
                                date,
                                self.config['calendar']['students_main_id'],
                                'חניכים כללי',
                                True)

        await self.looz_generic(context,
                                date,
                                self.config['calendar']['students_development_id'],
                                'חניכים פיתוח',
                                False)
        await self.looz_generic(context,
                                date,
                                self.config['calendar']['students_research_id'],
                                'חניכים מחקר',
                                False)
        await self.looz_generic(context,
                                date,
                                self.config['calendar']['students_firmware_id'],
                                'חניכים קושחה',
                                False)
        await self.looz_generic(context,
                                date,
                                self.config['calendar']['students_validation_id'],
                                'חניכים ולידציה',
                                False)

    @commands.hybrid_command(
        name="madrat",
        description="This command gives you today's madrat",
    )
    async def madrat(self, context: Context, day_offset: str = "0"):
        """
        This command gives you today's and tomorrow's madrat

        :param context: The application command context.
        :param day_offset: Integer offset in days to today
        """
        today = datetime.datetime.today()
        today = today + datetime.timedelta(days=int(day_offset))
        tomorrow = today + datetime.timedelta(days=1)

        madrat_today = list(calendar.get_daily_action_events(self.config['calendar']['segel_main_id'],
                                                             'מדרת',
                                                             today))
        madrat_tomorrow = list(calendar.get_daily_action_events(self.config['calendar']['segel_main_id'],
                                                                'מדרת',
                                                                tomorrow))

        async with aiohttp.ClientSession() as session:
            if not madrat_today:
                await context.send('לא נמצא מדר"ת להיום')
            else:
                madrat = discord_tools.match_channel_member(context, madrat_today[0][1][0])
                await context.send('המדר"ת להיום - ' + f'<@{madrat.id}>')

            if not madrat_tomorrow:
                await context.send('לא נמצא מדר"ת למחר')
            else:
                madrat = discord_tools.match_channel_member(context, madrat_tomorrow[0][1][0])
                await context.send('המדר"ת למחר - ' + f'<@{madrat.id}>')

    @commands.hybrid_command(
        name="nikayon",
        description="This command gives you today's 'toraney nikayon'",
    )
    async def nikayon(self, context: Context, day_offset: str = "0"):
        """
        This command gives you today's 'toraney nikayon'

        :param context: The application command context.
        """
        today = datetime.datetime.today()
        today = today + datetime.timedelta(days=int(day_offset))

        toranim_today = list(calendar.get_daily_action_events(self.config['calendar']['segel_main_id'],
                                                              'תורני ניקיון ופריסה',
                                                              today))

        async with aiohttp.ClientSession() as session:
            if not toranim_today:
                await context.send('לא נמצאו תורני ניקיון להיום')
                return

            message = 'תורני ניקיון ופריסה להיום - '
            _, toranim, _ = toranim_today[0]
            for toran in toranim:
                toran_member = discord_tools.match_channel_member(context, toran)
                if not toran_member:
                    await context.send(f'נמצאה שגיאה בשם אחד מתורני הניקיון - {toran}')
                    continue
                message += f'<@{toran_member.id}> '

            await context.send(message)

    @commands.hybrid_command(
        name="weekly",
        description="Daily greeting and mentions @everyone. Also reminds of Doh Ehad",
    )
    async def weekly(self, context: Context):
        """
        This command sends a daily greeting and mentions @everyone, for use in automation. Also reminds of Doh Ehad

        :param context: The application command context.
        """
        async with aiohttp.ClientSession() as session:
            await context.send('@everyone ' + 'שבוע טוב בי"ס מצוב!' + '\n' + 'לא לשכוח למלא דו"ח 1!')

    @commands.hybrid_command(
        name="daily",
        description="Daily greeting and mentions @everyone",
    )
    async def daily(self, context: Context):
        """
        This command sends a daily greeting and mentions @everyone, for use in automation

        :param context: The application command context.
        """
        async with aiohttp.ClientSession() as session:
            await context.send('@everyone ' + 'בוקר טוב בי"ס מצוב!')

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
