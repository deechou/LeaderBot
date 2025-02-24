import os
import discord
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
from classes import Leaderboard
from responses import *


# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("SERVER_ID")
LEADERBOARD_CHANNEL_ID = int(os.getenv("LEADERBOARD_CHANNEL_ID"))  # Channel where leaderboard message is posted
STATS_MSG_ID = int(os.getenv("MESSAGE_ID", "0"))  # Default to 0 if not set

# Initialize leaderboard
leaderboard = Leaderboard("Banana In-houses")

# Store leaderboard message object
leaderboard_message: Message = None

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

# # Step 2: MESSAGE FUNCTIONALITY
# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled)')
#         return
#
#     if is_private := user_message[0] == '?':
#         user_message = user_message[1:]
#
#     try:
#         response: str = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

# Sets up Leaderboard
@client.tree.command(name="setup_leaderboard", description="Sets up the leaderboard message", guild=GUILD_ID)
async def setup_leaderboard(interaction: discord.Interaction):
    global leaderboard_message
    channel = interaction.channel

    message = await channel.send("Initializing leaderboard...")
    leaderboard_message = message

    await interaction.response.send_message(f"Leaderboard setup complete! Message ID: {message.id}")

# Fetch stats message
@client.tree.command(name="fetch_leaderboard", description="Fetches leaderboard data from leaderboard message", guild=GUILD_ID)
async def fetch_leaderboard(interaction: discord.Interaction):
    global leaderboard_message
    channel = client.get_channel(LEADERBOARD_CHANNEL_ID)
    if channel and STATS_MSG_ID:
        try:
            leaderboard_message = await channel.fetch_message(STATS_MSG_ID)
            print("Leaderboard message fetched successfully.")
            print(leaderboard_message.content)
        except discord.NotFound:
            await interaction.response.send_message("Stats message not found. Run `/setup_leaderboard` to initialize.")
    else:
        print("Channel not found or MESSAGE_ID not set.")

# updates the leaderboard message with the leaderboard global
async def update_leaderboard_message():
    global leaderboard_message
    if leaderboard_message:
        leaderboard_content = leaderboard.print_by_wins()

        await leaderboard_message.edit(content=leaderboard_content)
    else:
        print("Leaderboard message not set. Please run '/setup_leaderboard' to initialize.")

@client.tree.command(name="addwin", description="Adds a win to a user", guild=GUILD_ID)
async def add_win(interaction: discord.Interaction, username: str):
    leaderboard.add_win(username)
    await update_leaderboard_message()
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