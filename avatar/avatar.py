from io import BytesIO
from typing import Optional

import discord
from discord.ext import commands


class Avatar:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx, user: Optional[discord.Member]):
        """ Check your avatar """
        if user:
            ext = "gif" if user.is_avatar_animated() else "png"
            e = discord.Embed(
                title=f"Here's the avatar of {user.name}", color=user.color
            )
            e.set_image(url=f"attachment://nevergonnagiveyouup.{ext}")
            e.set_footer(text=f"ID: {user.id}")
            await ctx.send(
                embed=e,
                file=discord.File(
                    BytesIO(await user.avatar_url.read()), f"nevergonnagiveyouup.{ext}"
                ),
            )
        else:
            user = ctx.author
            ext = "gif" if user.is_avatar_animated() else "png"
            e = discord.Embed(title=f"Here's your avatar {user.name}", color=user.color)
            e.set_image(url=f"attachment://nevergonnagiveyouup.{ext}")
            e.set_footer(text=f"ID: {user.id}")
            await ctx.send(
                embed=e,
                file=discord.File(
                    BytesIO(await user.avatar_url.read()), f"nevergonnagiveyouup.{ext}"
                ),
            )


def setup(bot):
    bot.add_cog(Avatar(bot))
