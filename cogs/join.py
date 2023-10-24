import discord
import logging
import redis

from discord.ext import commands
from .util.config import Config

log = logging.getLogger(__name__)


class JoinGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            if bot.auto_sync_commands:
                await self.bot.sync_commands()
            await self.config.setup_request(guild)
        except Exception as e:
            log.exception("on_guild_join,{0} error occured,{1}".format(type(e), e))


def setup(bot):
    bot.add_cog(JoinGuild(bot))
