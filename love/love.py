import bisect
import hashlib
import json
import logging
import random
from pathlib import Path
from typing import Union

import urllib
import discord
from discord import Member
from discord.ext import commands
from ext.command import command, group
from ext.utils import get_perm_level, get_command_level, owner
from discord.ext.commands import BadArgument, Cog, clean_content

log = logging.getLogger(__name__)

with open(Path(__file__).parent / "love_matches.json", "r", encoding="utf8") as file:
    LOVE_DATA = json.load(file)
    LOVE_DATA = sorted((int(key), value) for key, value in LOVE_DATA.items())


class LoveCal(Cog):
    """A cog for calculating the love between two people."""



    base_api_url = "https://api.martinethebot.com/v1"
    def ship_url(percent, {who}, {whom}):
      url = base_api_url + "/imagesgen/ship?precent=" + str({love_percent}) + "&first_user=" + urllib.urlencode({who}.avatar) + "&second_user=" + urllib.urlencode({whom}.avatar)
      return url   

    def __init__(self, bot: commands.Bot):
        self.bot = bot    

    @commands.command(aliases=('love_calculator', 'love_calc'))
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def love(self, ctx: commands.Context, who: Union[Member, str], whom: Union[Member, str] = None) -> None:
        """
        Tells you how much the two love each other.
        This command accepts users or arbitrary strings as arguments.
        """
        def normalize(arg: Union[Member, str]) -> str:
            if isinstance(arg, Member):
                arg = str(arg)
            else:
                arg = arg.strip().title()
            return clean_content(escape_markdown=True).convert(ctx, arg)

        who, whom = [await normalize(arg) for arg in (who, whom)]

        if not (who and whom):
            raise BadArgument('Arguments be non-empty strings.')

        m = hashlib.sha256(who.encode() + whom.encode())
        love_percent = sum(m.digest()) % 101


        base_api_url = "https://api.martinethebot.com/v1"
        def ship_url(percent, {who}, {whom}):
          url = base_api_url + "/imagesgen/ship?precent=" + str({love_percent}) + "&first_user=" + urllib.urlencode({who}.avatar) + "&second_user=" + urllib.urlencode({whom}.avatar)
          return url 

        index = bisect.bisect(LOVE_DATA, (love_percent,)) - 1
        _, data = LOVE_DATA[index]

        status = random.choice(data['titles'])
        embed = discord.Embed(
            title=status,
            description=f'{who} \N{HEAVY BLACK HEART} {whom} scored {love_percent}%!\n\u200b',
            color=discord.Color.dark_magenta()
        )
        embed.add_field(
            name='A letter from Dr. Love:',
            value=data['text']
        )
        embed.set_image(url=url)

        await ctx.send(embed=embed)