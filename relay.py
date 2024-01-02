import aiohttp
import discord
import os
import json
import re

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
SPY_CHANNELS = json.loads(os.environ.get("SPY_CHANNELS"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged on as {client.user}, tracking: ")
    for channel_id in SPY_CHANNELS:
        print(f" - {client.get_channel(channel_id)}")

    embed = discord.Embed(title="Discord relay completely started")
    channels = '\n'.join([client.get_channel(channel_id).name for channel_id in SPY_CHANNELS])
    embed.add_field(name="Channels observed:", value=channels)
    await send_embed_through_webhook(embed)

@client.event
async def on_message(message: discord.Message):
    if message.channel.id in SPY_CHANNELS and message.content:
        embed = discord.Embed(title=message.channel.guild.name)
        embed.add_field(name=message.channel.name, value=reformat_message(message))

        await send_embed_through_webhook(embed, member_mimic=message.author)

        for embed in message.embeds:
            await send_embed_through_webhook(embed)


async def send_embed_through_webhook(embed: discord.Embed, *, member_mimic: discord.Member = None):
    """
    Will send an embed to the discord webhook defined in the environment parameters potentially copying a user

    :param embed: A valid discord embed that will be the content of the message sent though the webhook
    :param member_mimic: A discord guild member that the webhook will copy the username/id
    """

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)

        if member_mimic is None:
            username = "Server Relay"
            avatar_url = None
        else:
            username =  member_mimic.display_name
            avatar_url = member_mimic.display_avatar.url

        await webhook.send(username=username, avatar_url=avatar_url, embed=embed)


def reformat_message(message: discord.Message) -> str:
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
            username = member_or_user_name_from_id(user_id, message.guild)
            message_content = message_content[:mention.span()[1]+offset] + f"({username})" + message_content[mention.span()[1]+offset:]
            offset += len(username) + 2

    if len(message_content) > 1024:
        message_content = message_content[:1021] + "..."

    return message_content

def member_or_user_name_from_id(user_id: int, guild: discord.Guild) -> str:
    """
    Will return the guild specific nick of the user if applicable or the standard username

    :param user_id: id of the discord user to search
    :param guild: Guild to check for specific nick. Default: None
    :return: String, name
    """

    if guild and (member := guild.get_member(user_id)) is not None:
        if (nick := member.nick) is not None:
            return nick

    if user := client.get_user(user_id):
        return user.name

    return "Name not found"


client.run(DISCORD_TOKEN)
