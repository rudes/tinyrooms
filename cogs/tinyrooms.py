import discord
import logging

from discord.ext import commands
from .util.config import Config

log = logging.getLogger(__name__)


class TinyRooms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            try:
                conf = self.config.get_all(member.guild.id)
            except Exception as e:
                await self.config.setup_request(member.guild)
                return
            cat = await member.guild.fetch_channel(conf["category_id"])

            for c in cat.channels:
                fresh = await member.guild.fetch_channel(conf["category_id"])
                if len(fresh.channels) == 1:
                    continue
                if len(c.members) == 0:
                    await c.delete(reason="everyone left")

            if member.voice and member.voice.channel.category == cat:
                opts = {"name": conf["channel_name"]}
                if conf["user_limit"] != 0:
                    opts["user_limit"] = conf["user_limit"]
                if conf["bitrate"] != 0:
                    opts["bitrate"] = conf["bitrate"]
                await cat.create_voice_channel(**opts)
        except Exception as e:
            log.exception("tinyrooms,{0} error occured,{1}".format(type(e), e))


def setup(bot):
    bot.add_cog(TinyRooms(bot))
