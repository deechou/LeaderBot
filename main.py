from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from classes import Score, Leaderboard

# Step -1: Connect to some database that keeps track of scores
leaderboard = Leaderboard("Banana In-houses")

# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
print(TOKEN)

# Step 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

# Step 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if "command" in response:
            if "won" in response:
                username = response.split(' ')[1]
                leaderboard.add_win(username)
                response_str = f"{username} won! Updating leaderboard..."
                await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            elif "lost" in response:
                username = response.split(' ')[1]
                leaderboard.add_loss(username)
                response_str = f"{username} lost! Updating leaderboard..."
                await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            elif "rankbywins" in response:
                response_str = leaderboard.print_by_wins()
                await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            elif "rankbywinrate" in response:
                response_str = leaderboard.print_by_winrate()
                await message.author.send(response_str) if is_private else await message.channel.send(response_str)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Step 3: HANDLING THE STARTUP FOR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Step 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Step 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()