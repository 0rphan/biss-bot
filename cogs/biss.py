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
        description="This command gives you today's and tomorrow's sahi",
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
            pretty_date = (datetime.datetime.now() +
                           datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            for row in csvreader:
                if row[0] == tomorrow:
                    embed = discord.Embed(
                        title="סח\"י",
                        description=f"הסח\"י לתאריך {pretty_date} זה {row[1]}",
                        color=0xD75BF4)
                    await context.send(embed=embed)
                    return
        embed = discord.Embed(description="אין סחי מחר", color=0xE02B2B)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Biss(bot))
