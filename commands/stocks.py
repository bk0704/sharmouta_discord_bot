from discord import app_commands, Embed
from discord.ext import commands
import finnhub
from utils.stocks_api import dividends
from dotenv import load_dotenv
import os


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='stock', description='Get stock price')
    async def stock(self, interaction, symbol: str):
        load_dotenv()
        finnhub_client = finnhub.Client(api_key=os.getenv('FINHUB_KEY'))
        res = finnhub_client.quote(symbol)
        if res:
            embed = Embed(
                title=f"Stock price for {symbol}",
                description=f"Current price: {res['c']}",
                color=0x1E90FF
            )
            embed.add_field(name="Open", value=res['o'], inline=False)
            embed.add_field(name="High", value=res['h'], inline=False)
            embed.add_field(name="Low", value=res['l'], inline=False)
            embed.add_field(name="Previous Close", value=res['pc'], inline=False)
            embed.set_footer(text="Data provided by Finnhub")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Failed to get stock price for {symbol}")

    @app_commands.command(name='stock_info', description='Get stock information')
    async def stock_info(self, interaction, symbol: str):
        load_dotenv()
        finnhub_client = finnhub.Client(api_key=os.getenv('FINHUB_KEY'))
        res = finnhub_client.company_profile2(symbol=symbol)
        if res:
            embed = Embed(
                title=f"Stock information for {symbol}",
                description=res['name'],
                color=0x1E90FF
            )
            embed.add_field(name="Country", value=res['country'], inline=False)
            embed.add_field(name="Currency", value=res['currency'], inline=False)
            embed.add_field(name="Exchange", value=res['exchange'], inline=False)
            embed.add_field(name="Industry", value=res['finnhubIndustry'], inline=False)
            embed.add_field(name="Market Cap", value=res['marketCapitalization'], inline=False)
            embed.add_field(name="IPO", value=res['ipo'], inline=False)
            embed.add_field(name="Web URL", value=res['weburl'], inline=False)
            embed.add_field(name="Phone Number", value=res['phone'], inline=False)
            embed.add_field(name="Outstanding Shares", value=res['shareOutstanding'], inline=False)
            embed.set_thumbnail(url=res['logo'])
            embed.set_footer(text="Data provided by Finnhub")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Failed to get stock information for {symbol}")

    @app_commands.command(name='symbol_search', description='Search for stock symbols')
    async def symbol_search(self, interaction, query: str):
        # Load API key
        load_dotenv()
        api_key = os.getenv('FINHUB_KEY')
        finnhub_client = finnhub.Client(api_key=api_key)

        # Call Finnhub's symbol lookup API
        res = finnhub_client.symbol_lookup(query)

        # Check if results exist
        if res and 'result' in res and len(res['result']) > 0:
            embed = Embed(
                title=f"Stock symbols for '{query}'",
                description="Here are the results:",
                color=0x1E90FF
            )

            # Iterate over the results
            for item in res['result']:
                embed.add_field(
                    name=item['description'],
                    value=f"Symbol: {item['symbol']}\nType: {item['type']}",
                    inline=False
                )

            embed.set_footer(text="Data provided by Finnhub")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"No results found for '{query}'", ephemeral=True)

    @app_commands.command(name='dividends', description='Get dividends for a stock')
    async def dividends(self, interaction, symbol: str):
        # Fetch dividends using the dividends function
        data = dividends(symbol)

        # Check if dividends were found
        if data:
            embed = Embed(
                title=f"Dividends for {symbol}",
                description="Here are the details:",
                color=0x1E90FF
            )
            embed.add_field(name="Amount", value=data['cash_amount'], inline=False)
            embed.add_field(name="Ex-Dividend Date", value=data['ex_dividend_date'], inline=False)
            embed.add_field(name="Payment Date", value=data['pay_date'], inline=False)
            embed.add_field(name="Record Date", value=data['record_date'], inline=False)
            embed.set_footer(text="Data provided by Polygon.io")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"No dividend information found for {symbol}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Stocks(bot))