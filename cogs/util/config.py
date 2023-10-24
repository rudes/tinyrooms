"""class for managing the Config"""
import logging
import json
import redis
import discord

log = logging.getLogger(__name__)


class ConfigModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Confirm?",
                placeholder="Yes",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, ctx: discord.Interaction):
        response = self.children[0].value.lower()
        if not response.startswith("y"):
            await ctx.response.send_message("Config not created.")
        cat = await ctx.guild.create_category("🚀 Tiny Rooms")
        chan = await cat.create_voice_channel(name="🚀 Tiny Room")
        conf = {
            "category_id": cat.id,
            "channel_name": chan.name,
            "user_limit": 0,
            "bitrate": 0,
        }
        db = redis.StrictRedis(host="db")
        db.set(str(ctx.guild.id), json.dumps(conf))
        await ctx.response.send_message("Config created.")


class Config:
    """class for managing the Config"""

    def __init__(self):
        self.db = redis.StrictRedis(host="db")

    def get(self, guild_id, setting):
        """get a specific value from the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        return config_json[setting]

    def get_all(self, guild_id):
        """get the full config from the db"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        return config_json

    def set(self, guild_id, setting, value):
        """set a specific value to the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        config_json[setting] = value
        config_string = json.dumps(config_json)
        self.db.set(str(guild_id), config_string)

    async def setup_guild(self, ctx):
        """prepare the discord for tinyrooms"""
        modal = ConfigModal(title="Create category and voice channel?")
        await ctx.send_modal(modal)

    async def setup_request(self, guild):
        """let people know to setup the bot"""
        chan = None
        for c in guild.text_channels:
            if c.permissions_for(guild.me).send_messages:
                chan = c
        if not chan:
            return
        message = "Thank you for adding 🚀 **Tiny Rooms**.\nTo setup have someone with admin rights use `/config setup`."
        async for m in chan.history(limit=100):
            if message == m.content:
                return
        await chan.send(message)
