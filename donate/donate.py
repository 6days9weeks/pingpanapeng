import discord
from discord.ext import commands


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            if "donate" in message.content.lower():
                await ctx.send(f"test")

def setup(bot):
    bot.add_cog(Donate(bot))
