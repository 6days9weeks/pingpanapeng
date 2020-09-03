import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class idk(commands.Cog):
    """
    Nothing Is Here
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["howto"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def helpie(self, ctx):
        """Explaination of commands"""
        embed = discord.Embed(
            title="How To Use Me- Brief Explanation"
        )
        embed.description = """
                **The commands are explained as followed -**
**To reply normally:** `!reply`,`!r` or <@!751098362580959232> r,
**To reply anonymously:** `!ar` or <@!751098362580959232> ar,
**To close a thread:** to close without any name or who did it just type `!close silently ~~reason~~` to close after sometime do `!close in 5m etc` ,
**To block a certain person from dming the bot:** `!block userid or usermention`,
**To get the loglink of this thread:** `!loglink`,
**To check logs of user:** `!logs user`,
**To make the bot say something:** `!say` only for owner,
**To delete a message:** `!delete messageid`,
**To open a thread with a person without them dming the bot:** `!contact userid or mention`,
**To get pinged if user replies in thread:** `!sub`,
**To make an embed:** `!a start` and follow the instructions.,
**To see the other available commands:** `!help`.
            """
        embed.color = self.bot.main_color
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(idk(bot))
