import os
import discord
import logging

from handlers import *
from discord.ext import commands

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
                    filename="/var/log/tinyrooms.log", level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.ERROR)

def main():
    bot = commands.Bot(intents=discord.Intents.all())
    bot.add_cog(tinyrooms.TinyRooms(bot))
    bot.run(str(os.environ['DISCORD_BOTKEY']))

if __name__ == "__main__":
    main()
