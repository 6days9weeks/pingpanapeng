import discord
from discord.ext import commands
import asyncio

class BanAppeal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_ready(self, thread):
        msg = thread.genesis_message

        def check(payload):
            return payload.emoji.name in "✅" and payload.message_id == msg.id and not payload.member.bot

        for emoji in "✅":
            await msg.add_reaction(emoji)

        try:
            payload = await self.bot.wait_for("raw_reaction_add", timeout=None, check=check)
        except asyncio.TimeoutError:
            pass

        else:
            if payload.emoji.name == "✅":
                try:
                    user = msg.guild.get_member(thread.recipient.id)
                    embed = discord.Embed(
                        title="Declined and Banned",
                        description=f"{payload.member.mention} declined {thread.recipient.mention}'s appeal.\n\n{thread.recipient.mention} has been banned.",
                        color=0x0000FF
                    )
                    await msg.channel.send(embed=embed)
                    await asyncio.sleep(2)
                    await thread.close(closer=payload.member)
                    await user.ban()
                except:
                    return await msg.channel.send(f"Couldn't Ban {thread.recipient}!L :(")


def setup(bot):
    bot.add_cog(BanAppeal(bot))
