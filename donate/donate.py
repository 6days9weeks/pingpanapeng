import discord
from discord.ext import commands


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

if message.channel.id == 692765490615156757:
            if "donate" in message.content.lower():
                await message.channel.send(f"....")

def setup(bot):
    bot.add_cog(Donate(bot))
