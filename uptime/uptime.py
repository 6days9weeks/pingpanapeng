import datetime

import discord
from core import checks
from core.decorators import trigger_typing
from core.models import PermissionLevel
from discord.ext import commands


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @trigger_typing
    async def uptime(self, ctx):
        """Shows uptime for the bot."""

        desc = "This is a command to view how long your bot has been "
        desc += "online since the last time it restarted."

        embed = discord.Embed(
            description=desc,
            color=self.bot.main_color,
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_author(
            name="Bot - Uptime",
            icon_url=self.bot.user.avatar_url,
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.add_field(name="Uptime", value=self.bot.uptime)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uptime(bot))
