import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class howto(commands.Cog):
    """
   A brief explanation on how the bot works.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["idkhowthisworks"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def howto(self, ctx):
        """A brief explanation on how the bot works"""
        embed = discord.Embed(
            title="How To Use Nezubabey"
        )
        embed.description = """
                **The commands are explained as followed -**\n**To reply normally:** `nezur` or <@742315489765621763> r,\n**To reply anonymously:** `nezuar` or <@742315489765621763> ar,\n**To close a thread:** to close without any name or who did it just type `nezuclose silenty ~~reason~~` to close after sometime do `nezuclose in 5m etc` ,\n**To block a certain person from dming the bot:** `nezublock userid or usermention`,\n**To get the loglink of this thread:** `nezuloglink`,\n**To check logs of user:** `nezulogs user`,\n**To make the bot say something:** `nezusay` only for owner,\n**To delete a message:** `nezudelete messageid`,\n**To open a thread with a person without them dming the bot:** `nezucontact userid or mention`,\n**To get pinged if user replies in thread:** `nezusubscribe`,\n**To add an tag:** `nezutags add "tag name" value`,\n\nAny questions? Just Dm or ping me my tag is `chizuru#0001` @chizuru#0001
            """
        embed.color = self.bot.main_color
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(howto(bot))
