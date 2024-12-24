import random

from discord import app_commands, Embed
from discord.ext import commands
from utils.education_apis import fetch_random_fact
from utils.education_apis import fetch_celestial_body
from utils.education_apis import fetch_country
import requests

class Education(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='fact', description='Get a random fact')
    async def fact(self, interaction):
        """
        Get a random fact.

        :param interaction:
        :return:
        """
        # Use the fetch_random_fact function to get a random fact
        fact = fetch_random_fact()

        # If no fact is found, send an error message
        if not fact:
            await interaction.response.send_message("Failed to get a random fact")
            return

        # Send the fact as a response
        await interaction.response.send_message(fact)

    @app_commands.command(name='word_of_the_day', description="Get the word of the day")
    async def word_of_the_day(self, interaction):
        word = 'Sharmouta: meaning slut in arabic "sharmout" can be used to describe a male gay guy and sharmouta is a female slut.'
        await interaction.response.send_message(word)

    @app_commands.command(name="celestial", description="Fetch details about a celestial body.")
    async def celestial(self, interaction, name: str):
        # Fetch data from the API logic
        data = fetch_celestial_body(name)

        # Handle errors
        if "error" in data:
            await interaction.response.send_message(f"Error: {data['error']}", ephemeral=True)
            return

        # Create an embed
        embed = Embed(
            title=f"Details about {data['name']}",
            description="Here is what I found:",
            color=0x1E90FF
        )
        embed.add_field(name="Mass", value=data["mass"], inline=False)
        embed.add_field(name="Gravity", value=data["gravity"], inline=False)
        embed.add_field(name="Mean Radius", value=data["radius"], inline=False)
        embed.add_field(name="Orbital Period", value=data["orbit"], inline=False)
        embed.add_field(name="Moons", value=", ".join(data["moons"]), inline=False)
        embed.set_footer(text="Data provided by Solar System OpenData API")

        # Send the embed
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="country", description="Fetch details about a country.")
    async def country(self, interaction, name: str):
        # Fetch data from the API logic
        data = fetch_country(name)

        # Handle errors
        if "error" in data:
            await interaction.response.send_message(f"Error: {data['error']}", ephemeral=True)
            return

        # Create an embed
        embed = Embed(
            title=f"Details about {data['name']['common']}",
            description="Here is what I found:",
            color=0x1E90FF
        )
        embed.add_field(name="Official Name", value=data["name"]["official"], inline=False)
        embed.add_field(name="Capital", value=data["capital"], inline=False)
        embed.add_field(name="Population", value=f"{data['population']:,}", inline=False)
        embed.add_field(name="Area", value=f"{data['area']:,} km²", inline=False)
        embed.add_field(name="Currency", value=data["currency"], inline=False)
        embed.add_field(name="Language", value=data["language"], inline=False)
        embed.set_thumbnail(url=data["flag"])
        embed.set_footer(text="Data provided by Rest Countries API")

        # Send the embed
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='quran', description='Get a random quran verse')
    async def quran(self, interaction):
        # command which sends a random quran verse when /quran is used
        verse_num = random.randint(1, 6236)
        try:
            # trys to request quran api for a random quran verse
            response = requests.get(
                "http://api.alquran.cloud/ayah/" + str(verse_num) + "/editions/quran-uthmani,en.pickthall")
            data = response.json()
            ar_verse = data["data"][0]["text"]
            en_verse = data["data"][1]["text"]
            surah = data["data"][0]["surah"]["englishName"]
            aya = data["data"][0]["numberInSurah"]

            await interaction.response.send_message(f"{ar_verse}\n\n{en_verse} - {surah}, {aya}")

        except Exception as e:
            print(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(Education(bot))