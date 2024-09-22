import discord
from discord.ext import commands
import os

# Definir variables de configuración directamente aquí o cargar desde un archivo de configuración
TOKEN = 'MTIxOTAxNjg5NjcyMTE5NTA0MA.G2aPUN.T2sQpbbHhUcfEjMIMPJntjFzZCPGE1j7_PD_RI'
CHANNEL_ID_ESTADO = '1275593106967761058'
GUILD_ID = '1272351854486884445'
CHANNEL_ID_GAMES = '1275593026260959368'
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'{filename} cargado correctamente.')
            except Exception as e:
                print(f'Error al cargar {filename}: {e}')
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')
    await load_cogs()
    await bot.tree.sync()
@bot.command()
async def check(self, ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{file_name}")
            await ctx.send(get_class(model_path="./keras_model.h5",label_path="./labels.txt",image_path="./{file_name}"))
    else:
        await ctx.send("Olvidaste subir una imagen 😞")

bot.run(TOKEN)