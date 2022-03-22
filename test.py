import discord
from utils import *


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id in SPY_CHANNELS and message.content:
            embed = discord.Embed(title=message.channel.guild.name)
            embed.set_author(name=message.author.display_name, icon_url=f'https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.webp')
            embed.add_field(name=message.channel.name, value=message.content)
            webhook = discord.Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN, adapter=discord.RequestsWebhookAdapter())

            webhook.send(embed=embed)


client = MyClient()
client.run(DISCORD_TOKEN)
