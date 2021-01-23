import typing

import aiohttp
import time
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pingt(self, ctx):
        """ Pong! """
        pings = []
        number = 0
        typings = time.monotonic()
        async with ctx.typing():
            typinge = time.monotonic()
        typingms = round((typinge - typings) * 1000)
        pings.append(typingms)
        latencyms = round(ctx.bot.latency * 1000)
        pings.append(latencyms)
        discords = time.monotonic()
        url = "https://discordapp.com/"
        async with aiohttp.ClientSession().get(url) as resp:
            if resp.status is 200:
                discorde = time.monotonic()
                discordms = round((discorde - discords) * 1000)
                pings.append(discordms)
                discordms = f"{discordms}ms"
            else:
                discordms = "Failed"
        for ms in pings:
            number += ms
        average = round(number / len(pings))
        await ctx.send(
            f"__**Pong:**__\nTyping: `{typingms}ms`  |  Latency: `{latencyms}ms`\nDiscord: `{discordms}`  |  Average: `{average}ms`"
        )


def setup(bot):
    bot.add_cog(Ping(bot))
