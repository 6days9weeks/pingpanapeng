
from dukpy import evaljs, JSRuntimeError
import re

from redbot.core.utils.chat_formatting import box

START_CODE_BLOCK_RE = re.compile(r"^((```js)(?=\s)|(```))")

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return START_CODE_BLOCK_RE.sub("", content)[:-3]

    # remove `foo`
    return content.strip("` \n")

@commands.command()
@checks.is_owner()
async def js(ctx, *, js: str):
    """Attempts to exec plain javascript."""
    async with ctx.typing():
        try:
            exec_shit = await bot.loop.run_in_executor(None, evaljs, cleanup_code(js))
        except JSRuntimeError as e:
            exec_shit = e
        await ctx.send(box(exec_shit, "js"))
    await ctx.tick()

return js
