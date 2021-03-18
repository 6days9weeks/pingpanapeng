import re

from discord.ext import commands
from dukpy import JSRuntimeError, evaljs

START_CODE_BLOCK_RE = re.compile(r"^((```js)(?=\s)|(```))")


def box(text: str, lang: str = "") -> str:
    """Get the given text in a code block.

    Parameters
    ----------
    text : str
        The text to be marked up.
    lang : `str`, optional
        The syntax highlighting language for the codeblock.

    Returns
    -------
    str
        The marked up text.

    """
    return "```{}\n{}\n```".format(lang, text)


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return START_CODE_BLOCK_RE.sub("", content)[:-3]

    # remove `foo`
    return content.strip("` \n")


class JS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def js(ctx, *, js: str):
        """Attempts to exec plain javascript."""
        async with ctx.typing():
            try:
                exec_shit = await bot.loop.run_in_executor(
                    None, evaljs, cleanup_code(js)
                )
            except JSRuntimeError as e:
                exec_shit = e
                await ctx.send(box(exec_shit, "js"))
            await ctx.message.add_reaction(":ok_hand:")


def setup(bot):
    bot.add_cog(JS(bot))
