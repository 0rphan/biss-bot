import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

import csv
import datetime


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
                        datetime.timedelta(days=1)).strftime("%-m/%d/%Y")
            today = (datetime.datetime.now()).strftime("%-m/%d/%Y")
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
