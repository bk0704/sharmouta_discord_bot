from random import randrange

from discord.ext import commands
from discord import app_commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kous', description='Check the bot\'s latency')
    async def ping(self, interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Imak {latency}ms')

    @app_commands.command(name='sharmouta', description='How much of a sharmouta are you?')
    async def sharmouta(self, interaction):
        sharmouta_level = randrange(0, 101)
        await interaction.response.send_message(f'You are {sharmouta_level}% sharmouta')

async def setup(bot):
    await bot.add_cog(Fun(bot))