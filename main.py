import os
import discord
from dotenv import load_dotenv
from discord import Intents, Message, app_commands, Interaction
from discord.ext import commands
from classes import Leaderboard



# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("SERVER_ID"))
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
            synced = await self.tree.sync(guild=discord.Object(id=GUILD_ID))
            print(f'Synced {len(synced)} commands to guild {GUILD_ID}!')

        except Exception as e:
            print(f'Failed to sync with guild {GUILD_ID}: {e}')

intents: Intents = Intents.default()
intents.message_content = True # NOQA

client: Client = Client(command_prefix="!", intents=intents)

# Sets up Leaderboard
@client.tree.command(name="setup_leaderboard", description="Sets up the leaderboard message", guild=discord.Object(id=GUILD_ID))
async def setup_leaderboard(interaction: discord.Interaction):
    global leaderboard_message
    channel = interaction.channel

    message = await channel.send("Initializing leaderboard...")
    leaderboard_message = message

    await interaction.response.send_message(f"Leaderboard setup complete! Message ID: {message.id}")

# Fetch stats message
@client.tree.command(name="fetch_leaderboard", description="Fetches leaderboard data from leaderboard message", guild=discord.Object(id=GUILD_ID))
async def fetch_leaderboard(interaction: discord.Interaction):
    global leaderboard_message
    global leaderboard
    channel = client.get_channel(LEADERBOARD_CHANNEL_ID)
    if channel and STATS_MSG_ID:
        try:
            leaderboard_message = await channel.fetch_message(STATS_MSG_ID)
            leaderboard = Leaderboard("Banana In-houses", leaderboard_message.content)
            print("Leaderboard message fetched successfully.")
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

@client.tree.command(name="addwin", description="Adds a win to a user", guild=discord.Object(id=GUILD_ID))
async def add_win(interaction: discord.Interaction, username: str):
    leaderboard.add_win(username)
    await update_leaderboard_message()
    await interaction.response.send_message(f'{username} won! Updating leaderboard...')

@client.tree.command(name="updatewins", description="Updates user's wins [username][wins]", guild=discord.Object(id=GUILD_ID))
async def update_wins(interaction: discord.Interaction, username: str, wins: int):
    leaderboard.change_wins(username, wins)
    await update_leaderboard_message()
    await interaction.response.send_message(f'Updating leaderboard for {username}...')

@client.tree.command(name="addloss", description="Adds a loss to a user", guild=discord.Object(id=GUILD_ID))
async def add_loss(interaction: discord.Interaction, username: str):
    leaderboard.add_loss(username)
    await update_leaderboard_message()
    await interaction.response.send_message(f'{username} lost! Updating leaderboard...')

@client.tree.command(name="updatelosses", description="Updates user's losses [username][losses]", guild=discord.Object(id=GUILD_ID))
async def update_wins(interaction: discord.Interaction, username: str, losses: int):
    leaderboard.change_losses(username, losses)
    await update_leaderboard_message()
    await interaction.response.send_message(f'Updating leaderboard for {username}...')

@client.tree.command(name="removewin", description="Removes a win from a user", guild=discord.Object(id=GUILD_ID))
async def remove_win(interaction: discord.Interaction, username: str):
    leaderboard.remove_win(username)
    await update_leaderboard_message()
    await interaction.response.send_message(f'removing win from {username}. Updating leaderboard...')

@client.tree.command(name="removeloss", description="Removes a loss from a user", guild=discord.Object(id=GUILD_ID))
async def remove_loss(interaction: discord.Interaction, username: str):
    leaderboard.remove_loss(username)
    await update_leaderboard_message()
    await interaction.response.send_message(f'removing loss from {username}. Updating leaderboard...')

@client.tree.command(name="removeplayer", description="Removes a player from the leaderboard", guild=discord.Object(id=GUILD_ID))
async def remove_player(interaction: discord.Interaction, username: str):
    leaderboard.remove_player(username)
    await update_leaderboard_message()
    await interaction.response.send_message(f'removing player: {username}. Updating leaderboard...')

@client.tree.command(name="rankbywins", description="Sorts Leaderboard by Number of Wins", guild=discord.Object(id=GUILD_ID))
async def rank_by_wins(interaction: discord.Interaction):
    await update_leaderboard_message()
    await interaction.response.send_message('Sorting leaderboard by amount of Wins...')

@client.tree.command(name="rankbywinrate", description="Sorts Leaderboard by Win percentage", guild=discord.Object(id=GUILD_ID))
async def rank_by_winrate(interaction: discord.Interaction):
    await update_leaderboard_message()
    await interaction.response.send_message('Sorting leaderboard by Win percentage...')

@client.tree.command(name="addtestdata", description="Adds test data for testing purposes", guild=discord.Object(id=GUILD_ID))
async def add_test_data(interaction: discord.Interaction):
    leaderboard.add_fake_data()
    await interaction.response.send_message('Adding fake data and updating message...')
    await update_leaderboard_message()

# Step 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()