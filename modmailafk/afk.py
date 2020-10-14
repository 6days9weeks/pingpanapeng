import discord
from core import Config, commands, checks
import typing 
import datetime
import re

IMAGE_LINKS = re.compile(r"(http[s]?:\/\/[^\"\']*\.(?:png|jpg|jpeg|gif|png))")


class Afk(commands.Cog):
    """le afk cog"""

    default_global_settings = {"ign_servers": []}
    default_guild_settings = {"TEXT_ONLY": False}
    default_user_settings = {
        "MESSAGE": False,
        "IDLE_MESSAGE": False,
        "DND_MESSAGE": False,
        "OFFLINE_MESSAGE": False,
        "GAME_MESSAGE": {},
        "STREAMING_MESSAGE": False,
        "LISTENING_MESSAGE": False,
    }


    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.away = dict()
    async def _set_db(self):
        user = await self.db.find_one({"_id": "user"})
        away = await self.db.find_one({"_id": "away"})

        if away is None:
            await self.db.find_one_and_update(
                {"_id": "away"}, {"$set": {"away": dict()}}, upsert=True
            )

            away = await self.db.find_one({"_id": "away"})

        if user is None:
            await self.db.find_one_and_update(
                {"_id": "user"},
                {
                    "$set": {
                        "id": dict(),
                    }
                },
                upsert=True,
            )

            config = await self.db.find_one({"_id": "user"})

        self.away = away.get("away", dict())
        self.id = user.get("id", dict())
        self.enabled = config.get("enabled", True)
        self.bot.loop.create_task(self._handle_away())

    async def _update_away(self):
        await self.db.find_one_and_update(
            {"_id": "away"}, {"$set": {"away": self.away}}, upsert=True
        )

    async def _update_user(self):
        await self.db.find_one_and_update(
            {"_id": "user"},
            {
                "$set": {
                    "id": self.id,
                }
            },
            upsert=True,
        )
    def _draw_play(self, song):
        song_start_time = song.start
        total_time = song.duration
        current_time = datetime.datetime.utcnow()
        elapsed_time = current_time - song_start_time
        sections = 12
        loc_time = round((elapsed_time / total_time) * sections)  # 10 sections

        bar_char = "\N{BOX DRAWINGS HEAVY HORIZONTAL}"
        seek_char = "\N{RADIO BUTTON}"
        play_char = "\N{BLACK RIGHT-POINTING TRIANGLE}"
        msg = "\n" + play_char + " "

        for i in range(sections):
            if i == loc_time:
                msg += seek_char
            else:
                msg += bar_char

        msg += " `{:.7}`/`{:.7}`".format(str(elapsed_time), str(total_time))
        return msg

    async def make_embed_message(self, author, message, state=None):
        """
            Makes the embed reply
        """
        avatar = author.avatar_url_as()  # This will return default avatar if no avatar is present
        color = author.color
        if message:
            link = IMAGE_LINKS.search(message)
            if link:
                message = message.replace(link.group(0), " ")
        if state == "away":
            em = discord.Embed(description=message, color=color)
            em.set_author(name=f"{author.display_name} is currently afk", icon_url=avatar)
        elif state == "idle":
            em = discord.Embed(description=message, color=color)
            em.set_author(name=f"{author.display_name} is currently idle", icon_url=avatar)
        elif state == "dnd":
            em = discord.Embed(description=message, color=color)
            em.set_author(name=f"{author.display_name} is currently do not disturb", icon_url=avatar)
        elif state == "offline":
            em = discord.Embed(description=message, color=color)
            em.set_author(name=f"{author.display_name} is currently offline", icon_url=avatar)
        elif state == "gaming":
            em = discord.Embed(description=message, color=color)
            em.set_author(
                name=f"{author.display_name} is currently playing {author.activity.name}", icon_url=avatar,
            )
            em.title = getattr(author.activity, "details", None)
            thumbnail = getattr(author.activity, "large_image_url", None)
            if thumbnail:
                em.set_thumbnail(url=thumbnail)
        elif state == "gamingcustom":
            status = [c for c in author.activities if c.type == discord.ActivityType.playing]
            em = discord.Embed(description=message, color=color)
            em.set_author(
                name=f"{author.display_name} is currently playing {status[0].name}", icon_url=avatar,
            )
            em.title = getattr(status[0], "details", None)
            thumbnail = getattr(status[0], "large_image_url", None)
            if thumbnail:
                em.set_thumbnail(url=thumbnail)
        elif state == "listening":
            em = discord.Embed(color=author.activity.color)
            url = f"https://open.spotify.com/track/{author.activity.track_id}"
            artist_title = f"{author.activity.title} by " + ", ".join(
                a for a in author.activity.artists
            )
            limit = 256 - (
                len(author.display_name) + 27
            )  # incase we go over the max allowable size
            em.set_author(
                name=f"{author.display_name} is currently listening to",
                icon_url=avatar,
                url=url,
            )
            em.description = (
                f"{message}\n "
                f"[{artist_title}]({url})\n"
                f"{self._draw_play(author.activity)}"
            )

            em.set_thumbnail(url=author.activity.album_cover_url)
        elif state == "listeningcustom":
            activity = [c for c in author.activities if c.type == discord.ActivityType.listening]
            em = discord.Embed(color=activity[0].color)
            url = f"https://open.spotify.com/track/{activity[0].track_id}"
            artist_title = f"{activity[0].title} by " + ", ".join(a for a in activity[0].artists)
            limit = 256 - (len(author.display_name) + 27)
            em.set_author(
                name=f"{author.display_name} is currently listening to",
                icon_url=avatar,
                url=url
            )
            em.description = (
                f"{message}\n "
                f"[{artist_title}]({url})\n"
                f"{self._draw_play(activity[0])}"
            )
            em.set_thumbnail(url=activity[0].album_cover_url)
        elif state == "streaming":
            color = int("6441A4", 16)
            em = discord.Embed(color=color)
            em.description = message + "\n" + author.activity.url
            em.title = getattr(author.activity, "details", None)
            em.set_author(
                name=f"{author.display_name} is currently streaming {author.activity.name}", icon_url=avatar,
            )
        elif state == "streamingcustom":
            activity = [c for c in author.activities if c.type == discord.ActivityType.streaming]
            color = int("6441A4", 16)
            em = discord.Embed(color=color)
            em.description = message + "\n" + activity[0].url
            em.title = getattr(author.activity, "details", None)
            em.set_author(
                name=f"{author.display_name} is currently streaming {activity[0].name}", icon_url=avatar,
            )
        else:
            em = discord.Embed(color=color)
            em.set_author(name="{} is currently afk".format(author.display_name), icon_url=avatar)
        if link and state not in ["listening", "listeningcustom", "gaming"]:
            em.set_image(url=link.group(0))
        return em

    async def find_user_mention(self, message):
        """
            Replaces user mentions with their username
        """
        for word in message.split():
            match = re.search(r"<@!?([0-9]+)>", word)
            if match:
                user = await self.bot.fetch_user(int(match.group(1)))
                message = re.sub(match.re, "@" + user.name, message)
        return message

    async def make_text_message(self, author, message, state=None):
        """
            Makes the message to display if embeds aren't available
        """
        message = await self.find_user_mention(message)

        if state == "away":
            msg = f"{author.display_name} is currently afk"
        elif state == "idle":
            msg = f"{author.display_name} is currently idle"
        elif state == "dnd":
            msg = f"{author.display_name} is currently do not disturb"
        elif state == "offline":
            msg = f"{author.display_name} is currently offline"
        elif state == "gaming":
            msg = f"{author.display_name} is currently playing {author.activity.name}"
        elif state == "gamingcustom":
            status = [c for c in author.activities if c.type == discord.ActivityType.playing]
            msg = f"{author.display_name} is currently playing {status[0].name}"
        elif state == "listening":
            artist_title = f"{author.activity.title} by " + ", ".join(a for a in author.activity.artists)
            currently_playing = self._draw_play(author.activity)
            msg = f"{author.display_name} is currently listening to {artist_title}\n{currently_playing}"
        elif state == "listeningcustom":
            status = [c for c in author.activities if c.type == discord.ActivityType.listening]
            artist_title = f"{status[0].title} by " + ", ".join(a for a in status[0].artists)
            currently_playing = self._draw_play(status[0])
            msg = f"{author.display_name} is currently listening to {artist_title}\n{currently_playing}"
        elif state == "streaming":
            msg = f"{author.display_name} is currently streaming at {author.activity.url}"
        elif state == "streamingcustom":
            status = [c for c in author.activities if c.type == discord.ActivityType.streaming]
            msg = f"{author.display_name} is currently streaming at {status[0].url}"
        else:
            msg = f"{author.display_name} is currently afk"

        if message != " " and state != "listeningcustom":
            msg += f" and has set the following message: `{message}`"
        elif message != " " and state == "listeningcustom":
            msg += f"\n\nCustom message: `{message}`"

        return msg

    async def is_mod_or_admin(self, member: discord.Member):
        guild = member.guild
        if member == guild.owner:
            return True
        if await self.bot.is_owner(member):
            return True
        if await self.bot.is_admin(member):
            return True
        if await self.bot.is_mod(member):
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        tmp = {}
        guild = message.guild
        list_of_guilds_ign = await self._away.ign_servers()
        if not guild:
            return
        if not message.channel.permissions_for(guild.me).send_messages:
            return
        if not message.mentions:
            return
        if message.author.bot:
            return

        for author in message.mentions:
            if guild.id in list_of_guilds_ign and not await self.is_mod_or_admin(author):
                continue
            user_data = await self._away.user(author).all()
            text_only = await self._away.guild(guild).TEXT_ONLY()
            embed_links = message.channel.permissions_for(guild.me).embed_links

            away_msg = user_data["MESSAGE"]
            if away_msg:
                if type(away_msg) in [tuple, list]:
                    # This is just to keep backwards compatibility
                    away_msg, delete_after = away_msg
                else:
                    delete_after = None
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, away_msg, "away")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, away_msg, "away")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            idle_msg = user_data["IDLE_MESSAGE"]
            if idle_msg and author.status == discord.Status.idle:
                if type(idle_msg) in [tuple, list]:
                    idle_msg, delete_after = idle_msg
                else:
                    delete_after = None
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, idle_msg, "idle")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, idle_msg, "idle")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            dnd_msg = user_data["DND_MESSAGE"]
            if dnd_msg and author.status == discord.Status.dnd:
                if type(dnd_msg) in [tuple, list]:
                    dnd_msg, delete_after = dnd_msg
                else:
                    delete_after = None
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, dnd_msg, "dnd")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, dnd_msg, "dnd")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            offline_msg = user_data["OFFLINE_MESSAGE"]
            if offline_msg and author.status == discord.Status.offline:
                if type(offline_msg) in [tuple, list]:
                    offline_msg, delete_after = offline_msg
                else:
                    delete_after = None
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, offline_msg, "offline")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, offline_msg, "offline")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            streaming_msg = user_data["STREAMING_MESSAGE"]
            if streaming_msg and type(author.activity) is discord.Streaming:
                streaming_msg, delete_after = streaming_msg
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, streaming_msg, "streaming")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, streaming_msg, "streaming")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            if streaming_msg and type(author.activity) is discord.CustomActivity:
                stream_status = [c for c in author.activities if c.type == discord.ActivityType.streaming]
                if not stream_status:
                    continue
                streaming_msg, delete_after = streaming_msg
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, streaming_msg, "streamingcustom")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, streaming_msg, "streamingcustom")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            listening_msg = user_data["LISTENING_MESSAGE"]
            if listening_msg and type(author.activity) is discord.Spotify:
                listening_msg, delete_after = listening_msg
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, listening_msg, "listening")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, listening_msg, "listening")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            if listening_msg and type(author.activity) is discord.CustomActivity:
                listening_status = [c for c in author.activities if c.type == discord.ActivityType.listening]
                if not listening_status:
                    continue
                listening_msg, delete_after = listening_msg
                if embed_links and not text_only:
                    em = await self.make_embed_message(author, listening_msg, "listeningcustom")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and text_only) or not embed_links:
                    msg = await self.make_text_message(author, listening_msg, "listeningcustom")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
            gaming_msgs = user_data["GAME_MESSAGE"]
            if gaming_msgs and type(author.activity) in [discord.Game, discord.Activity]:
                for game in gaming_msgs:
                    if game in author.activity.name.lower():
                        game_msg, delete_after = gaming_msgs[game]
                        if embed_links and not text_only:
                            em = await self.make_embed_message(author, game_msg, "gaming")
                            await message.channel.send(embed=em, delete_after=delete_after)
                            break  # Let's not accidentally post more than one
                        elif (embed_links and text_only) or not embed_links:
                            msg = await self.make_text_message(author, game_msg, "gaming")
                            await message.channel.send(msg, delete_after=delete_after)
                            break
            if gaming_msgs and type(author.activity) is discord.CustomActivity:
                game_status = [c for c in author.activities if c.type == discord.ActivityType.playing]
                if not game_status:
                    continue
                for game in gaming_msgs:
                    if game in game_status[0].name.lower():
                        game_msg, delete_after = gaming_msgs[game]
                        if embed_links and not text_only:
                            em = await self.make_embed_message(author, game_msg, "gamingcustom")
                            await message.channel.send(embed=em, delete_after=delete_after)
                            break  # Let's not accidentally post more than one
                        elif (embed_links and text_only) or not embed_links:
                            msg = await self.make_text_message(author, game_msg, "gamingcustom")
                            await message.channel.send(msg, delete_after=delete_after)
                            break

    @commands.command(name="afk")
    async def away_(self, ctx, delete_after: Optional[int] = None, *, message: str = None):
        """
        Tell the bot you're afk or back.
        `delete_after` Optional seconds to delete the automatic reply
        `message` The custom message to display when you're mentioned
        """
        author = ctx.message.author
        mess = await self._away.user(author).MESSAGE()
                    away_obj = {}
                    away_obj["mess"] = int(away[0])
                    self.away[str(ctx.author.id)] = away_obj
        if mess:
            await self._away.user(author).MESSAGE.set(False)
            msg = "You're now back."
        else:
            if message is None:
                await self._away.user(author).MESSAGE.set((" ", delete_after))
            else:
                await self._away.user(author).MESSAGE.set((message, delete_after))
            msg = "You're now set as afk."
        await ctx.send(msg)

    @commands.command()
    @checks.admin_or_permissions(administrator=True)
    async def afktextonly(self, ctx):
        """
        Toggle forcing the guild's away messages to be text only.
        This overrides the embed_links check this cog uses for message sending.
        """
        text_only = await self._away.guild(ctx.guild).TEXT_ONLY()
        if text_only:
            message = "Afk messages will now be embedded or text only based on the bot's permissions for embed links."
        else:
            message = (
                "Afk messages are now forced to be text only, regardless of the bot's permissions for embed links."
            )
        await self._away.guild(ctx.guild).TEXT_ONLY.set(not text_only)
        await ctx.send(message)