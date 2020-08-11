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
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def helpie(self, ctx):
        """Explaination of commands"""
        embed = discord.Embed(
            title="How To"
        )
        embed.description = """
                **The commands are explained as followed -**
**To reply normally:** `nezur` or <@742315489765621763> r,
**To reply anonymously:** `nezuar` or <@742315489765621763> ar,
**To close a thread:** to close without any name or who did it just type `nezuclose silenty ~~reason~~` to close after sometime do `nezuclose in 5m etc` ,
**To block a certain person from dming the bot:** `nezublock userid or usermention`,
**To get the loglink of this thread:** `nezuloglink`,
**To check logs of user:** `nezulogs user`,
**To make the bot say something:** `nezusay` only for owner,
**To delete a message:** `nezudelete messageid`,
**To open a thread with a person without them dming the bot:** `nezucontact userid or mention`,
**To get pinged if user replies in thread:** `nezusubscribe`,
**To add an tag:** `nezutags add "tag name" value`,
Any questions? Just Dm or ask me my tag is `chizuru#0001` <@682849186227552266>
            """
        embed.color = self.bot.main_color
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(idk(bot))
