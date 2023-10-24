import logging
import discord

from discord import SlashCommandGroup, ApplicationContext
from discord.ext import commands
from discord.commands import Option
from .util.config import Config

log = logging.getLogger(__name__)


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    config = SlashCommandGroup(
        "config",
        "Setup server and change settings for temporary channels.",
        checks=[commands.has_permissions(administrator=True).predicate],
    )

    @config.command(name="setup")
    async def setup_guild(
        self,
        ctx: ApplicationContext,
    ):
        try:
            await self.config.setup_guild(ctx)
        except Exception as e:
            log.exception(f"setup_guild,{type(e)} error occured,{e}")
            await ctx.respond("Failed to setup the Server.")

    @config.command(name="view")
    async def view_config(
        self,
        ctx: ApplicationContext,
    ):
        try:
            conf = self.config.get_all(ctx.guild.id)
            await ctx.respond(f"{conf}")
        except Exception as e:
            log.exception(f"setup_guild,{type(e)} error occured,{e}")
            await ctx.respond("Failed to get the Config. Try `/config setup`.")

    @config.command(name="set_name")
    async def set_channel_name(
        self,
        ctx: ApplicationContext,
        name: Option(str),
    ):
        """Set the name used for all temporary channels"""
        try:
            self.config.set(ctx.guild.id, "channel_name", name)
            await ctx.respond(f"Changed channel name to {name}")
        except Exception as e:
            log.exception(f"set_channel_name,{type(e)} error occured,{e}")
            await ctx.respond("Failed to set the channel name.")

    @config.command(name="set_user_limit")
    async def set_user_limit(
        self,
        ctx: ApplicationContext,
        limit: Option(int),
    ):
        """Set the user limit for all temporary channels"""
        try:
            self.config.set(ctx.guild.id, "user_limit", limit)
            await ctx.respond(f"Changed user limit to {limit}")
        except Exception as e:
            log.exception(f"set_user_limit,{type(e)} error occured,{e}")
            await ctx.respond("Failed to set the user limit.")

    @config.command(name="set_bitrate")
    async def set_bitrate(
        self,
        ctx: ApplicationContext,
        bitrate: Option(int),
    ):
        """Set the bitrate for all temporary channels"""
        try:
            self.config.set(ctx.guild.id, "bitrate", bitrate)
            await ctx.respond(f"Changed bitrate to {bitrate}")
        except Exception as e:
            log.exception(f"set_bitrate,{type(e)} error occured,{e}")
            await ctx.respond("Failed to set the bitrate.")


def setup(bot):
    bot.add_cog(Settings(bot))
