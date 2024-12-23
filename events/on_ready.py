from discord.ext import commands
import discord

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'ready_called'):
            self.bot.ready_called = True

            # Log bot's status
            print(f'{self.bot.user} has connected to Discord!')
            print ("Connected to the following guilds:")
            for guild in self.bot.guilds:
                print(f'{guild.name} (id: {guild.id})')

            # Set the bot's activity
            activity = discord.Game(name = "/help to view commands")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)

            # Log command tree readiness
            print("Bot is operational")

async def setup(bot):
    await bot.add_cog(OnReady(bot))