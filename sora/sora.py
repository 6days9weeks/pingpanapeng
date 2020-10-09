from core import checks
import discord
from core.models import PermissionLevel
from discord.ext import commands,tasks
import asyncio

class StatusChiasa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def start_status(self):
        server = self.bot.get_guild(699158208027164723)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{server.member_count} Members🎃 🥀!"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=f"DM For Help/Report", url="https://twitch.tv/kawaiii0001"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Sponsor Us | By Hosting Giveaways"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"❥sasha is a bad coder"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Chiasa | DM For Help | {server.member_count} Members🎃 🥀"))
        await asyncio.sleep(10)

    @commands.command(name="ss")
    @checks.has_permissions(PermissionLevel.OWNER)
    async def start_start_cmd(self, ctx):
        self.start_status.start()
        await ctx.message.add_reaction("<a:tickn:739397501693591563>")
        embed = discord.Embed(title="Error", description="This command can only be used by **❥sasha**!", color=0xffc2ff)
        await ctx.send(embed=embed, delete_after=5.0)

def setup(bot):
    bot.add_cog(StatusChiasa(bot))
