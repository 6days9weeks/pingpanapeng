import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class PMRole(commands.Cog):
    """Provides commands for giving/taking away pm role in a thread"""
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["pmrole"], invoke_without_command=True)
    async def pm_role(self, ctx):
        """Checks the pm role"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['roles']
            await ctx.send(embed=discord.Embed(description="The pm role is <@&"+roles['pm']+">", color=0x9b59b6))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="There isn't a pm role set\nAdmins can set it with `pm_role set [role]`", color=0x9b59b6))

    @pm_role.command(name="set")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def partner_role_set(self, ctx, *, role: discord.Role):
        """Sets the pm role"""
        await self.db.find_one_and_update(
            {'_id': 'config'},
            {'$set': {'roles': {'pm': str(role.id)}}},
            upsert=True
        )
        await ctx.send(embed=discord.Embed(description="The pm role is now "+role.mention, color=0x9b59b6))
    
    @commands.command(aliases=["apm", "addpm"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def add_pm(self, ctx):
        """Adds the pm role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['roles']
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).add_roles(ctx.guild.get_role(int(roles['pm'])), reason="Role added by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]")
                await ctx.send(embed=discord.Embed(description="Added <@&"+roles['pm']+"> to "+ctx.thread.recipient.mention, color=0x9b59b6))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to add <@&"+roles['pm']+"> to "+ctx.thread.recipient.mention, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Pm role not found", color=0xff0000))
    
    @commands.command(aliases=["rpm", "removepm"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def remove_pm(self, ctx):
        """Removes the pm role from the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['roles']
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).remove_roles(ctx.guild.get_role(int(roles['pm'])), reason="Role removed by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]") 
                await ctx.send(embed=discord.Embed(description="Removed <@&"+roles['pm']+"> from "+ctx.thread.recipient.mention, color=0x9b59b6))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to remove <@&"+roles['pm']+"> from "+ctx.thread.recipient.mention, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Pm role not found", color=0xff0000))

def setup(bot):
    bot.add_cog(PMRole(bot))
