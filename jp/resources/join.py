import discord

from .timedelta import format_time


class MemberResource:
    def __init__(self, ctx, member):
        self.ctx = ctx
        self.member = member

        self._get_member()
        if self.member is None:
            try:
                self.member = discord.utils.get(self.ctx.guild.members, id=int(self.ctx.channel.topic[9:]))
                if self.member is None:
                    self.member = self.ctx.author
            except (ValueError, TypeError):
                self.member = self.ctx.author

    def _get_member(self):
        """Fetch a member by its name or nickname."""

        if isinstance(self.member, discord.Member):
            return

        if self.member is None:
            self.member = None
            return

        for m in self.ctx.guild.members:
            if m.display_name.lower().startswith(self.member.lower()):
                self.member = m
                return

            if m.name.lower().startswith(self.member.lower()):
                self.member = m
                return

        self.member = None

    def member_embed(self):
        """Create an embed containing the member's information."""
        join_position = sorted(m.guild.members, key=lambda m: m.joined_at).index(m) + 1

        embed = discord.Embed(color=m.color)

        embed.set_author(name=f"{str(m)}'s Join Position")        
        embed.add_field(name="You are our member no.", value=join_position)
        
        return embed
