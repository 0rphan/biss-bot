import aiohttp
import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, calendar


class Biss(commands.Cog, name="biss"):

    def __init__(self, bot):
        self.bot = bot

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
        description="This command gives you today's looz",
    )
    @checks.not_blacklisted()
    async def looz(self, context: Context):
        """"
        This command gives you today's looz

        :param context: The application command context.
        """
        events = calendar.get_daily_events()
        if events is None:
            return
        if not events:
            async with aiohttp.ClientSession() as session:
                embed = discord.Embed(
                    description='אין לו"ז להיום! חבורת חפשנים!', color=0xD75BF4)
                await context.send(embed=embed)
            return

        start_times = ''
        end_times = ''
        summaries = ''

        if events:
            for event in events:
                is_all_day = bool(event["start"].get("dateTime", False))
                if not is_all_day:
                    date = event["start"]["date"]
                    start_times += f'{date}\n'
                    end_times += 'כל היום\n'
                else:
                    start_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                    end_time = datetime.datetime.fromisoformat(event["end"]["dateTime"])
                    start_hour = start_time.strftime('%H:%M')
                    end_hour = end_time.strftime('%H:%M')
                    start_times += f'{start_hour}\n'
                    end_times += f'{end_hour}\n'
                summaries += f'{event["summary"]}\n'

        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(
                title='הלו"ז להיום:', color=0xD75BF4)
            embed.add_field(name='התחלה', value=start_times, inline=True)
            embed.add_field(name='סיום', value=end_times, inline=True)
            embed.add_field(name='תיאור', value=summaries, inline=True)
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
