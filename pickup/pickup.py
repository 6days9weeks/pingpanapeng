import logging
import random
from json import load
from pathlib import Path

import discord
from redbot.core import commands

log = logging.getLogger(__name__)

with open(Path(__file__).parent / "pickup_lines.json", "r", encoding="utf8") as f:
    pickup_lines = load(f)


class PickupLine(commands.Cog):
    """A cog that gives random cheesy pickup lines."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pickupline(self, ctx: commands.Context) -> None:
        """
        Gives you a random pickup line.
        Note that most of them are very cheesy.
        """
        random_line = random.choice(pickup_lines["lines"])
        embed = discord.Embed(
            title=":cheese: Your pickup line :cheese:",
            description=random_line["line"],
            color=0xFFC2FF,
        )
        embed.set_thumbnail(url=random_line.get("image", pickup_lines["placeholder"]))
        await ctx.send(embed=embed)
