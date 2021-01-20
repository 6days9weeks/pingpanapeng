from .spookyrating import SpookyRating


def setup(bot):
    bot.add_cog(SpookyRating(bot))
