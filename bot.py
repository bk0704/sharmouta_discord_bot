from fileinput import filename

import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

# Create a bot instance
class Sharmouta(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Load cogs dynamically
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'commands.{filename[:-3]}')
                    print (f"Loaded command cog: {filename}")
                except Exception as e:
                    print(f"Failed to load cog {filename}: {e}")

        # Load event handlers
        for filename in os.listdir('./events'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'events.{filename[:-3]}')
                    print(f"Loaded event handler: {filename}")
                except Exception as e:
                    print(f"Failed to load event handler {filename}: {e}")


        # Sync slash commands
        try:
            if GUILD_ID:
                guild = discord.Object(id=int(GUILD_ID))
                await self.tree.sync(guild=guild)
                print('Commands synced to guild')
            else:
                await self.tree.sync()
                print('Commands synced globally')
            # Debug: Print all registered commands
            print("Registered commands:")
            for cmd in self.tree.get_commands():
                print(f"- {cmd.name}: {cmd.description}")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

bot = Sharmouta()
bot.run(TOKEN)

