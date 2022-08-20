import discord
import os
import json


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
SPY_CHANNELS = json.loads(os.environ.get("SPY_CHANNELS"))
WEBHOOK_ID = os.environ.get("WEBHOOK_ID")
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id in SPY_CHANNELS and message.content:
            embed = discord.Embed(title=message.channel.guild.name)
            embed.set_author(name=message.author.display_name, icon_url=f'https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.webp')
            embed.add_field(name=message.channel.name, value=message.content[:1024])
            webhook = discord.Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN, adapter=discord.RequestsWebhookAdapter())

            webhook.send(embed=embed)


client = MyClient()
client.run(DISCORD_TOKEN)
