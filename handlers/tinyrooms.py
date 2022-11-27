import discord
import logging

from discord.ext import commands

log = logging.getLogger(__name__)

class TinyRooms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            for chan in self.bot.get_all_channels():
                if type(chan) is not discord.CategoryChannel or chan.name != 'Tiny Rooms':
                    continue
                scale_cat = await self.bot.fetch_channel(chan.id)
                for c in scale_cat.channels:
                    fresh_scale_cat = await self.bot.fetch_channel(chan.id)
                    if len(fresh_scale_cat.channels) == 1:
                        continue
                    if len(c.members) == 0:
                        await c.delete(reason='everyone left')
                if member.voice and member.voice.channel.category == scale_cat:
                    await scale_cat.create_voice_channel(name='🚀 Tiny Room')
        except Exception as e:
            log.error('tinyrooms,{0} error occured,{1}'.format(type(e), e))
