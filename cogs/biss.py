import json
import datetime
from pathlib import Path

import aiohttp
import discord

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, calendar


class Biss(commands.Cog, name="biss"):

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
        DATE_FORMAT = '%d-%m-%Y'
        TIME_FORMAT = '%H:%M'

        if not date:
            date = datetime.datetime.today().strftime(DATE_FORMAT)

        events = calendar.get_daily_events(self.config['calendar_id'], datetime.datetime.strptime(date, DATE_FORMAT))
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
                if datetime.datetime.strptime(date, DATE_FORMAT) < datetime.datetime.strptime(start, '%Y-%m-%d'):
                    continue
                end = 'כל היום'
            else:
                start_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                end_time = datetime.datetime.fromisoformat(event["end"]["dateTime"])
                start_hour = start_time.strftime(TIME_FORMAT)
                end_hour = end_time.strftime(TIME_FORMAT)
                start = start_hour
                end = end_hour
            embed.add_field(name='',
                            value=f'{start} - {end} : {event["summary"]}',
                            inline=False)

        async with aiohttp.ClientSession() as session:
            await context.send(embed=embed)

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
