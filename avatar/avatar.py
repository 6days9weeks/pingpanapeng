import aiohttp
import discord
import asyncio
from discord.ext import commands
import os
import io
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import pagify, box

class Avatar:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, member:discord.Member=None):
        async with ctx.channel.typing():
            if member is None:
                member = ctx.message.author
            if member.is_avatar_animated():
                async with self.session.get(member.avatar_url_as(format="gif")) as resp:
                    data = await resp.read()
                file = discord.File(io.BytesIO(data),filename="{}.gif".format(member.name))
            if not member.is_avatar_animated():
                async with self.session.get(member.avatar_url_as(static_format="png")) as resp:
                    data = await resp.read()
                file = discord.File(io.BytesIO(data),filename="{}.png".format(member.name))
            await ctx.send(file=file)   
