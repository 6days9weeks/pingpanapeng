import discord
from core import checks
from core.models import PermissionLevel
from discord.ext import commands


class StaffRoles(commands.Cog):
    """Provides commands for giving/taking away staff roles in a thread"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["staffrole"], invoke_without_command=True)
    async def staff_role(self, ctx):
        """Checks the staff role"""
        try:
            roles = ((await self.db.find_one({"_id": "config"})) or {})["roles"]
            await ctx.send(
                embed=discord.Embed(
                    description="The staff role is <@&" + roles["staff"] + ">",
                    color=0xD0B8D6,
                )
            )
        except KeyError:
            await ctx.send(
                embed=discord.Embed(
                    description="There isn't a staff role set\nAdmins can set it with `staff_role set [role]`",
                    color=0xD0B8D6,
                )
            )

    @staff_role.command(name="set")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def staff_role_set(self, ctx, *, role: discord.Role):
        """Sets the staff role"""
        await self.db.find_one_and_update(
            {"_id": "config"},
            {"$set": {"staffrole": {"staff": str(role.id)}}},
            upsert=True,
        )
        await ctx.send(
            embed=discord.Embed(
                description="The staff role is now " + role.mention, color=0xD0B8D6
            )
        )

    @commands.group(aliases=["helperrole"], invoke_without_command=True)
    async def helper_role(self, ctx):
        """Checks the helper role"""
        try:
            roles = ((await self.db.find_one({"_id": "config"})) or {})["helper"]
            await ctx.send(
                embed=discord.Embed(
                    description="The helper role is <@&" + roles["helper"] + ">",
                    color=0xD0B8D6,
                )
            )
        except KeyError:
            await ctx.send(
                embed=discord.Embed(
                    description="There isn't a helper role set\nAdmins can set it with `helper_role set [role]`",
                    color=0xD0B8D6,
                )
            )

    @helper_role.command(name="set")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def helper_role_set(self, ctx, *, role: discord.Role):
        """Sets the helper role"""
        await self.db.find_one_and_update(
            {"_id": "config"},
            {"$set": {"helperrole": {"helper": str(role.id)}}},
            upsert=True,
        )
        await ctx.send(
            embed=discord.Embed(
                description="The helper role is now " + role.mention, color=0xD0B8D6
            )
        )

    @commands.command(aliases=["addstaff"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def add_staff(self, ctx):
        """Adds the staff role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({"_id": "config"})) or {})["staffrole"]
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).add_roles(
                    ctx.guild.get_role(int(roles["staff"])),
                    reason="Role Added By Echidna",
                )
                await ctx.send(
                    embed=discord.Embed(
                        description="Added <@&"
                        + roles["staff"]
                        + "> to "
                        + ctx.thread.recipient.mention,
                        color=0xD0B8D6,
                    )
                )
            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        description="Failed to add <@&"
                        + roles["staff"]
                        + "> to "
                        + ctx.thread.recipient.mention,
                        color=0xD0B8D6,
                    )
                )
        except KeyError:
            await ctx.send(
                embed=discord.Embed(description="staff role not found", color=0xD0B8D6)
            )

    @commands.command(aliases=["addhelper"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def add_helper(self, ctx):
        """Adds the staff role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({"_id": "config"})) or {})["helperrole"]
            try:

                await ctx.guild.get_member(ctx.thread.recipient.id).add_roles(
                    ctx.guild.get_role(int(roles["helper"])),
                    reason="Role Added By Echidna",
                )
                await ctx.send(
                    embed=discord.Embed(
                        description="Added <@&"
                        + roles["helper"]
                        + "> to "
                        + ctx.thread.recipient.mention,
                        color=0xD0B8D6,
                    )
                )
            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        description="Failed to add <@&"
                        + roles["helped"]
                        + "> to "
                        + ctx.thread.recipient.mention,
                        color=0xD0B8D6,
                    )
                )
        except KeyError:
            await ctx.send(
                embed=discord.Embed(description="helper role not found", color=0xD0B8D6)
            )


def setup(bot):
    bot.add_cog(StaffRoles(bot))
