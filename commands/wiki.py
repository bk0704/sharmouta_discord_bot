from discord import app_commands
from discord.ext import commands
from utils.wikipedia_api import search_wikipedia
from utils.wikipedia_api import get_random_article
from utils.wikipedia_api import get_trending_articles
from utils.wikipedia_api import get_article_categories
from utils.wikipedia_api import get_article_sections
import discord

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='wiki', description='Search Wikipedia for an article')
    async def wiki(self, interaction, topic: str):
        """
        Search Wikipedia for an article on the given topic.

        :param interaction:
        :param topic:
        :return:
        """
        # Use the search_wikipedia function to find the article
        result = search_wikipedia(topic)

        # If no results are found, send an error message
        if not result:
            await interaction.response.send_message(f"No results found for '{topic}'")
            return

        # Create an embed for the result
        embed = discord.Embed(
            title=result['title'],
            description=result['snippet'],
            url=result['url'],
            color=discord.Color.blue()
        )
        if result['image_url']:
            embed.set_thumbnail(url=result['image_url'])
        embed.set_footer(text="Powered by Wikipedia")

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='random_wiki', description='Get a random Wikipedia article')
    async def random_wiki(self, interaction):
        """
        Get a random Wikipedia article.

        :param interaction:
        :return:
        """
        # Use the get_random_article function to find a random article
        result = get_random_article()

        # If no results are found, send an error message
        if not result:
            await interaction.response.send_message("Failed to get a random article")
            return

        # Create an embed for the result
        embed = discord.Embed(
            title=result['title'],
            url=result['url'],
            color=discord.Color.blue()
        )
        if result['image']:
            embed.set_thumbnail(url=result['image'])
        embed.set_footer(text="Powered by Wikipedia")

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="trending_wiki", description="Fetch trending articles on Wikipedia")
    async def trending_wiki(self, interaction):
        results = get_trending_articles()
        if not results:
            await interaction.response.send_message("Failed to fetch trending articles. Please try again later.")
            return

        embed = discord.Embed(
            title="Trending Wikipedia Articles",
            description="Here are the top trending articles on Wikipedia:",
            color=discord.Color.purple()
        )
        for result in results:
            embed.add_field(name=result['title'], value=result['url'], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wiki_categories", description="Fetch categories of a Wikipedia article")
    async def wiki_categories(self, interaction, title: str):
        categories = get_article_categories(title)
        if not categories:
            await interaction.response.send_message(f"No categories found for the article '{title}'.")
            return

        embed = discord.Embed(
            title=f"Categories for '{title}'",
            description="\n".join(categories),
            color=discord.Color.orange()
        )
        embed.set_footer(text="Powered by Wikipedia")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wiki_sections", description="Fetch sections of a Wikipedia article")
    async def wiki_sections(self, interaction, title: str):
        sections = get_article_sections(title)
        if not sections:
            await interaction.response.send_message(f"No sections found for the article '{title}'.")
            return

        embed = discord.Embed(
            title=f"Sections for '{title}'",
            description="\n".join([f"{section['level']}: {section['title']}" for section in sections]),
            color=discord.Color.teal()
        )
        embed.set_footer(text="Powered by Wikipedia")

        await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(Wiki(bot))