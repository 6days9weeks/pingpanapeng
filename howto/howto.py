import datetime

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.decorators import trigger_typing


class Howto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @trigger_typing
    async def howto(self, ctx):
        """Help command in brief"""

        desc = "Just an easy explanation on how the bot works"
        desc += "this is just the tip of the iceberg this bot can do much moreee."

        embed = discord.Embed(
            description=desc,
            color=self.bot.main_color,
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_author(
            name="How To Use Nezubabey",
            icon_url=self.bot.user.avatar_url,
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.add_field(name="Explanation", value=**The commands are explained as followed -**\n**To reply normally:** `nezur` or @nezubabey#2849 r,\n**To reply anonymously:** `nezuar` or @nezubabey#2849 ar,\n**To close a thread:** to close without any name or who did it just type `nezuclose silenty ~~reason~~` to close after sometime do `nezuclose in 5m etc` ,\n**To block a certain person from dming the bot:** `nezublock userid or usermention`,\n**To get the loglink of this thread:** `nezuloglink`,\n**To check logs of user:** `nezulogs user`,\n**To make the bot say something:** `nezusay` only for owner,\n**To delete a message:** `nezudelete messageid`,\n**To open a thread with a person without them dming the bot:** `nezucontact userid or mention`,\n**To get pinged if user replies in thread:** `nezusubscribe`,\n**To add an tag:** `nezutags add "tag name" value`,\n\nAny questions? Just Dm or ask me my tag is `chizuru#0001` <@!682849186227552266>)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Howto(bot))
