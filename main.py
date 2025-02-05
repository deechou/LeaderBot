from typing import Final
import os

import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands
from discord.ext import commands
from responses import get_response
from classes import Score, Leaderboard

# Step -1: Connect to some database that keeps track of scores
leaderboard = Leaderboard("Banana In-houses")

# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
SERVER_ID: Final[str] = os.getenv("SERVER_ID")
GUILD_ID = discord.Object(id=SERVER_ID)

# Step 1: BOT SETUP
class Client(commands.Bot):
    # HANDLING THE STARTUP FOR BOT
    async def on_ready(self) -> None:
        print(f'{self.user} is now running!')

        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to guild {GUILD_ID}!')

        except Exception as e:
            print(f'Failed to sync with guild {GUILD_ID}: {e}')

    # HANDLING INCOMING MESSAGES
    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message)


intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(command_prefix="!", intents=intents)

# Step 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if "!command" in response:
            cmd = response.split(' ')[1]
            args = response.split(' ')[2:]
            # if cmd == "addwin":
            #     username = args[0]
            #     leaderboard.add_win(username)
            #     response_str = f"{username} won! Updating leaderboard..."
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # if cmd == "addloss":
            #     username = args[0]
            #     leaderboard.add_loss(username)
            #     response_str = f"{username} lost! Updating leaderboard..."
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # if cmd == "removewin":
            #     username = args[0]
            #     leaderboard.remove_win(username)
            #     response_str = f"removing win from {username}. Updating leaderboard..."
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # elif cmd == "removeloss":
            #     username = args[0]
            #     leaderboard.remove_loss(username)
            #     response_str = f"removing loss from {username}. Updating leaderboard..."
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # elif cmd == "removeplayer":
            #     username = args[0]
            #     leaderboard.remove_player(username)
            #     response_str = f"removing player: {username}. Updating leaderboard..."
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # elif cmd == "rankbywins":
            #     response_str = leaderboard.print_by_wins()
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
            # elif cmd == "rankbywinrate":
            #     response_str = leaderboard.print_by_winrate()
            #     await message.author.send(response_str) if is_private else await message.channel.send(response_str)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.tree.command(name="hello", description="Say hello", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="addwin", description="Adds a win to a user", guild=GUILD_ID)
async def add_win(interaction: discord.Interaction, username: str):
    leaderboard.add_win(username)
    await interaction.response.send_message(f'{username} won! Updating leaderboard...')

@client.tree.command(name="addloss", description="Adds a loss to a user", guild=GUILD_ID)
async def add_loss(interaction: discord.Interaction, username: str):
    leaderboard.add_loss(username)
    await interaction.response.send_message(f'{username} lost! Updating leaderboard...')

@client.tree.command(name="removewin", description="Removes a win from a user", guild=GUILD_ID)
async def remove_win(interaction: discord.Interaction, username: str):
    leaderboard.remove_win(username)
    await interaction.response.send_message(f'removing win from {username}. Updating leaderboard...')

@client.tree.command(name="removeloss", description="Removes a loss from a user", guild=GUILD_ID)
async def remove_loss(interaction: discord.Interaction, username: str):
    leaderboard.remove_loss(username)
    await interaction.response.send_message(f'removing loss from {username}. Updating leaderboard...')

@client.tree.command(name="removeplayer", description="Removes a player from the leaderboard", guild=GUILD_ID)
async def remove_player(interaction: discord.Interaction, username: str):
    leaderboard.remove_player(username)
    await interaction.response.send_message(f'removing player: {username}. Updating leaderboard...')

@client.tree.command(name="rankbywins", description="Sorts Leaderboard by Number of Wins", guild=GUILD_ID)
async def rank_by_wins(interaction: discord.Interaction):
    await interaction.response.send_message(leaderboard.print_by_wins())

@client.tree.command(name="rankbywinrate", description="Sorts Leaderboard by Win percentage", guild=GUILD_ID)
async def rank_by_winrate(interaction: discord.Interaction):
    await interaction.response.send_message(leaderboard.print_by_winrate())


# Step 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()