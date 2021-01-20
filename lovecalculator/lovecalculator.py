from io import BytesIO

import aiohttp
import discord
from discord.ext import commands


class LoveCalculator(commands.Cog):
    """Calculate the love percentage for two users!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def ship(
        self,
        ctx,
        user1: discord.Member,
        user2: Optional[discord.Member],
        use_nicks: bool = False,
    ):
        """Ship names of 2 server members and count their compatibility level."""
        if not user2:
            user2 = ctx.author
            user1, user2 = user2, user1
        if not use_nicks:
            member_name_one = user1.name[: len(user1.name) // 2]
            member_name_two = user2.name[len(user2.name) // 2 :]
        else:
            member_name_one = user1.display_name[: len(user1.display_name) // 2]
            member_name_two = user2.display_name[len(user2.display_name) // 2 :]
        random.seed(user1.id + user2.id)
        love_level = random.randint(0, 100)

        async with ctx.typing():
            try:
                async with aiohttp.ClientSession().get(
                    "https://api.martinebot.com/v1/imagesgen/ship",
                    params={
                        "percent": love_level,
                        "first_user": str(user1.avatar_url_as(format="png")),
                        "second_user": str(user2.avatar_url_as(format="png")),
                    },
                    raise_for_status=True,
                ) as r:
                    pic = BytesIO(await r.read())
            except aiohttp.ClientResponseError as e:
                pic = (
                    f"Unable to get image: [{e.status}] {e.message}\n\nTry again later."
                )
            e = discord.Embed(
                title=f"{member_name_one}{member_name_two}",
                description=chat.inline(("█" * round(love_level / 4)).ljust(25))
                + f" {love_level}%",
                color=await ctx.embed_color(),
            )
            if isinstance(pic, BytesIO):
                e.set_image(url="attachment://compatibility.png")
                e.set_footer(
                    text="Fufu, so cute.",
                    icon_url="https://cdn.discordapp.com/emojis/773581891156443166.png?v=1",
                )
            elif isinstance(pic, str):
                e.set_footer(text=pic)
            await ctx.send(
                embed=e,
                file=discord.File(pic, filename="compatibility.png") if pic else None,
            )
            if isinstance(pic, BytesIO):
                pic.close()

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def betterosu(self, ctx, user):
        osu_user = f"{user}"
        async with aiohttp.ClientSession().get(
            "https://api.martinebot.com/v1/imagesgen/osuprofile",
            params={
                "player_username": osu_user,
            },
            raise_for_status=True,
        ) as r:
            pic = BytesIO(await r.read())
        e = discord.Embed(
            title=f"Here's the osu profile for {user}", color=discord.Color.random()
        )
        if isinstance(pic, BytesIO):
            e.set_image(url="attachment://osu.png")
        elif isinstance(pic, str):
            e.set_footer(text="Api is currently down.")

        await ctx.send(
            embed=e,
            file=discord.File(pic, filename="osu.png") if pic else None,
        )
        if isinstance(pic, BytesIO):
            pic.close()


def setup(bot):
    bot.add_cog(LoveCalculator(bot))
