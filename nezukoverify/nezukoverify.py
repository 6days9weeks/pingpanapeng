import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class CatFish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["selfyrol"], invoke_without_command=True)
    async def selfy_role(self, ctx):
        """Checks the selfie verify role"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['nezuroles']
            await ctx.send(embed=discord.Embed(description="The verified role is <@&"+roles['selfy']+">", color=0xffc2ff))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="There isn't a verified role set\nAdmins can set it with `selfy_role set [role]`", color=0xffc2ff))

    @selfy_role.command(name="set")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def selfy_role_set(self, ctx, *, role: discord.Role):
        """Sets the selfie verified role"""
        await self.db.find_one_and_update(
            {'_id': 'config'},
            {'$set': {'nezuroles': {'selfy': str(role.id)}}},
            upsert=True
        )
        await ctx.send(embed=discord.Embed(description="The selfie verified role is now "+role.mention, color=0xffc2ff))
    
    @commands.command(aliases=["aselfie", "sfy"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def sverify(self, ctx):
        """Adds the selfie verified role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['nezuroles']
            try:
                await self.bot.guild.get_member(ctx.thread.recipient.id).add_roles(self.bot.guild.get_role(int(roles['selfy'])), reason="Role added by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]")
                await ctx.send(embed=discord.Embed(description="Added <@&"+roles['selfy']+"> to "+ctx.thread.recipient.mention, color=0xffc2ff))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to add <@&"+roles['selfy']+"> to "+ctx.thread.recipient.mention, color=0xffc2ff))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Selfie verified role not found", color=0xffc2ff))
    
def setup(bot):
    bot.add_cog(CatFish(bot))

