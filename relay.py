import discord
import os
import json
import re

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
SPY_CHANNELS = json.loads(os.environ.get("SPY_CHANNELS"))
WEBHOOK_ID = int(os.environ.get("WEBHOOK_ID"))
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}, tracking: ")
        for channel_id in SPY_CHANNELS:
            print(f" - {self.get_channel(channel_id)}")

    async def on_message(self, message: discord.Message):
        webhook = discord.Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN, adapter=discord.RequestsWebhookAdapter())

        if message.channel.id in SPY_CHANNELS and message.content:
            embed = discord.Embed(title=message.channel.guild.name)
            embed.add_field(name=message.channel.name, value=self.reformat_message(message))

            webhook.send(username=message.author.display_name,
                         avatar_url=f'https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.webp',
                         embeds=[embed] + message.embeds[:9])

    def reformat_message(self, message: discord.Message) -> str:
        """
        Reformat the message to improve mentions and make sure it's short enough (can't be more than 1024 chars)
        :param message: discord message to reformat
        :return: message content reworked
        """

        message_content = message.content
        user_mentions = re.finditer(r'<@\d{18}>', message_content)
        offset = 0
        for mention in user_mentions:
            user_id = 0
            try:
                user_id = int(mention.group(0)[2:20])
            except ValueError:
                pass

            if user_id:
                username = self.member_or_user_name_from_id(user_id, message.guild)
                message_content = message_content[:mention.span()[1]+offset] + f"({username})" + message_content[mention.span()[1]+offset:]
                offset += len(username) + 2

        if len(message_content) > 1024:
            message_content = message_content[:1021] + "..."

        return message_content

    def member_or_user_name_from_id(self, user_id: int, guild: discord.Guild) -> str:
        """
        Will return the guild specific nick of the user if applicable or the standard username

        :param user_id: id of the discord user to search
        :param guild: Guild to check for specific nick. Default: None
        :return: String, name
        """

        if guild and (member := guild.get_member(user_id)) is not None:
            if (nick := member.nick) is not None:
                return nick

        if user := self.get_user(user_id):
            return user.name

        return "Name not found"


client = MyClient()
client.run(DISCORD_TOKEN)
