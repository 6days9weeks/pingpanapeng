from .love import LoveCal

__red_end_user_data_statement__ = (
    "This cog stores data provided by users "
    "for the express purpose of redisplaying. "
    "It does not store user data which was not "
    "provided through a command. "
)


def setup(bot):
    bot.add_cog(LoveCal(bot))
