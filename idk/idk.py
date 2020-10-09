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
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(aliases=["howto"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def helpie(self, ctx):
        """Explaination of commands"""
        embed = discord.Embed(
            title="How To Use Nezubabey- Brief Explanation"
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
**To selfie verify a member:** `nezusverify` in the modmail channel.
Any questions? Just ping me in chat my tag is `❥sasha#0001` <@682849186227552266>
            """
        embed.color = self.bot.main_color
        return await ctx.send(embed=embed)

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

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def mmkkjj(self, ctx, role: discord.Role, member: discord.Member=None):
        """Assign a role to a member."""
        if member is None:
            try:
                member = ctx.guild.get_member(int(ctx.channel.topic[9:]))
            except (ValueError, TypeError):
                raise commands.MissingRequiredArgument(SimpleNamespace(name="role"))
        
        if role.position > ctx.author.roles[-1].position:
            return await ctx.send("You do not have permissions to give this role.")
        
        await member.add_roles(role)
        await ctx.send(f"Successfully added the role to {member.name}!")          
            
def setup(bot):
    bot.add_cog(idk(bot))
