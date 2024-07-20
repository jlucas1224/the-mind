import discord
import responses


async def send_message(username, message, user_message, is_private):
    try:
        response = await responses.handle_response(message, username, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    token = 'MTI2Mzk1MTkxNjIxNjM1Mjc3OQ.G3Qee7.E5MKPdfUVPnBjZwgg31NVG-hlss5eXv5kKEyvk'
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '!':
            user_message = user_message[1:]
            await send_message(username, message, user_message, is_private=True)
        else:
            await send_message(username, message, user_message, is_private=False)

    client.run(token)
