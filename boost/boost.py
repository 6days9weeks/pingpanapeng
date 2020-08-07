import discord
from discord.ext import commands
class Boost(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        print(message.type)
        if message.type == discord.MessageType.premium_guild_subscription:
            embed = discord.Embed(title=f"**Nitro Boost**", description=f"Thank you so much for boosting <a:BoostingAnimated:717651091260702751> !", color=0xff0000)
            m = await message.channel.send(embed=embed)
            await m.add_reaction("<a:Heartanimated:717651074126708756>")
            
def setup(bot):
    bot.add_cog(Boost(bot))
