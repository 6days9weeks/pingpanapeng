
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class CatFish(commands.Cog):
    """Provides commands for verifying a member in a thread"""
    def __init__(self, bot):
        self.bot = bot
        self.verified = 760529072655958077

    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def sverify(self, ctx):
        """Adds the verified selfie role to the thread recipient"""
        try:
            roles = guild.get_role(self.verified)
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).add_roles(ctx.guild.get_role((roles)), reason="Role added by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]")
                await ctx.send(embed=discord.Embed(description="Added <@&"+roles+"> to "+ctx.thread.recipient.mention, color=0xffcff2))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to add <@&"+roles['pm']+"> to "+ctx.thread.recipient.mention, color=0xffcff2))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Failed to add role", color=0xffcff2))
    

def setup(bot):
    bot.add_cog(CatFish(bot))
