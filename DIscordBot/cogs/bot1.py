import discord
from discord.ext import commands
from discord import app_commands
import random

class ServerGames(commands.Cog):
    def __init__(self, bot, channel_id_games):
        self.bot = bot
        self.channel_id_games = channel_id_games

    @app_commands.command(name="8ball", description="Gira la bola mágica")
    async def _8ball(self, interaction: discord.Interaction, pregunta: str):
        ball = ("sí", "no", "probablemente", "no sé", "quizá")
        respuesta = random.choice(ball)

        embed = discord.Embed(title="8Ball", description="La bola mágica ha escogido:", color=discord.Color.blue())
        embed.add_field(name="Tu pregunta:", value=f"{pregunta}", inline=False)
        embed.add_field(name="Respuesta", value=f"{respuesta}", inline=False)

        try:
            await interaction.response.send_message(embed=embed)
        except discord.errors.InteractionResponded:
            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    channel_id_games = '1275593026260959368'  # Cambia este valor si es necesario
    await bot.add_cog(ServerGames(bot, channel_id_games))
