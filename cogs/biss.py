import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

import csv


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
            for row in csvreader:
                print(row)
        embed = discord.Embed(description="sahi", color=0xD75BF4)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Biss(bot))
