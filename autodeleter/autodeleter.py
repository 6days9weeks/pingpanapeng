from discord.ext import commands


class Autodeleter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # for s special server only lol
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 757144854265331792:

            await message.delete()


def setup(bot):
    bot.add_cog(Autodeleter(bot))
