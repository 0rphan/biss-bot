import discord
from discord.ext.commands import Context

def get_channel_members(context: Context) -> list[discord.Member]:
    guild = context.message.channel.guild
    return guild.members

def match_channel_member(context: Context, nickname: str) -> discord.Member:
    members = get_channel_members(context)
    for member in members:
        if member.display_name.count(' ') == 0:
            continue

        _, member_name = tuple(member.display_name.split(' ', 1))
        if member_name == nickname:
            return member