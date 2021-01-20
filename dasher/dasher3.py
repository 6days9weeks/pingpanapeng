import asyncio

import discord
from discord.ext import commands


class Dasher3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.maincolor = 0x06C9FF
        self.errorcolor = 0xFF0000
        self.Role1 = 752919582414471349  # ID of the Discord Member role

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:
            if message.channel.id == 752919997621338272:
                if message.content.lower() == "!role ap":
                    guild = message.guild
                    role = guild.get_role(self.Role1)

                    await message.author.add_roles(role)

                    await message.add_reaction("\U00002705")

                    await asyncio.sleep(2)
                    await message.delete()
                    try:
                        embed = discord.Embed(
                            title="Role Given",
                            description="You now have the activity role now go chat",
                            color=self.maincolor,
                        )
                        embed.set_thumbnail(url=message.author.avatar_url)
                        await message.author.send(embed=embed)
                    except:
                        print(
                            f"Couldn't send {message.author.name} his verification acceptation"
                        )

                else:
                    await message.delete()
                    return


def setup(bot):
    bot.add_cog(Dasher3(bot))
