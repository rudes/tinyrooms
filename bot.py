import os
import logging
import discord

from discord.ext import commands

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
    filename="/var/log/discord/tinyrooms.log",
    level=logging.INFO,
)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

discord_log = logging.getLogger("discord")
discord_log.setLevel(logging.ERROR)

bot = commands.Bot(
    intents=discord.Intents.all(),
    debug_guilds=[int(os.environ["DEBUG_GUILD_ID"])],
)

bot.load_extensions("cogs")
bot.run(str(os.environ["DISCORD_BOTKEY"]))
