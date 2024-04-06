import aiohttp
import discord
from discord.ext import tasks, commands
from discord.ext.commands import Context

from helpers import checks

import csv
import datetime

def get_sahi() -> str:
    """ This command gives you today's and tomorrow's 'sahi' """
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

        return desc


class Biss(commands.Cog, name="biss"):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="info",
        description="This command gives info about a student",
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
        name="sahi",
        description="This command gives you today's and tomorrow's 'sahi'",
    )
    @checks.not_blacklisted()
    async def sahi(self, context: Context):
        """
        This command gives you today's and tomorrow's sahi

        :param context: The application command context.
        """
        desc = get_sahi()

        if desc:
            embed = discord.Embed(
                title="אקטואליה יומית",
                description=desc,
                color=0xD75BF4)
            await context.send(embed=embed)
            return

        embed = discord.Embed(description="אין 'אקטואליה יומית' היום או מחר", color=0xE02B2B)
        await context.send(embed=embed)


    # @tasks.loop(time=datetime.time(hour=7, minute=30))
    @tasks.loop(time=datetime.time(hour=7, minute=30))
    async def daily_sahi(self):
        """
        This command gives you today's and tomorrow's sahi.
        Almost everyday at 7:30 AM.
        """
        print("AUTO SAHI")

        if datetime.datetime.now().strftime('%A').lower() in ["friday", "saturday"]:
            print("No auto-sahi on the weekend.")
            # return

        print("JK JK")

        channel = self.bot.get_channel("1214585866966532146") # 1214585866966532146
        channel2 = self.bot.get_channel("1214585867578908688") # 1214585867578908688

        print(channel, channel2)
        print(type(channel), type(channel2))

        desc = get_sahi()
        print(f"desc: {desc}")

        if desc:
            embed = discord.Embed(
                title="אקטואליה יומית",
                description=desc,
                color=0xD75BF4)
            await channel.send(embed=embed)
            return

        embed = discord.Embed(description="אין 'אקטואליה יומית' היום או מחר", color=0xE02B2B)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Biss(bot))
