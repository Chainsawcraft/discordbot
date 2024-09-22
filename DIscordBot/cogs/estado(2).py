import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer

class ServerStatus(commands.Cog):
    def __init__(self, bot, channel_id_estado):
        self.bot = bot
        self.channel_id_estado = channel_id_estado
        self.status_message = None
        self.seconds_until_next_update = 0
        self.update_timer.start()
        self.send_server_status.start()

    def get_server_status(self, host, port):
        server = JavaServer(host, port)
        try:
            status = server.status()
            return True, f"El servidor está en línea: {status.players.online} jugadores en línea"
        except Exception as e:
            return False, f"El servidor está fuera de línea o no se puede conectar: {str(e)}"

    @tasks.loop(minutes=1)
    async def send_server_status(self):
        await self.update_status_message()

    @tasks.loop(seconds=1)
    async def update_timer(self):
        if self.seconds_until_next_update > 0:
            self.seconds_until_next_update -= 1
            if self.status_message:
                await self.update_status_message(edit=True)

    async def update_status_message(self, edit=False):
        channel = self.bot.get_channel(int(self.channel_id_estado))
        if channel is None:
            print("Canal no encontrado en Discord.")
            return
        
        velocity_online, _ = self.get_server_status("nova.hidencloud.com", 25868)
        lobby_online, _ = self.get_server_status("uk01.legacynodes.com", 2015)
        survival_online, _ = self.get_server_status("free.whost.es", 10634)

        next_update_in = self.send_server_status.next_iteration - discord.utils.utcnow()
        self.seconds_until_next_update = int(next_update_in.total_seconds())

        embed = discord.Embed(title="Estado De La Network", description="Aquí tendrás el estado en breve:", color=discord.Color.blue())
        embed.add_field(name="Velocity", value="🟢" if velocity_online else "🔴", inline=False)
        embed.add_field(name="Lobby", value="🟢" if lobby_online else "🔴", inline=False)
        embed.add_field(name="Survival", value="🟢" if survival_online else "🔴", inline=False)
        embed.add_field(name="Se actualiza en", value=f"{self.seconds_until_next_update} segundos", inline=False)

        if not edit:
            if self.status_message:
                try:
                    await self.status_message.delete()
                except discord.NotFound:
                    print("El mensaje que se intenta eliminar no se encuentra.")
            self.status_message = await channel.send(embed=embed)
        else:
            if self.status_message:
                try:
                    await self.status_message.edit(embed=embed)
                except discord.NotFound:
                    print("El mensaje que se intenta editar no se encuentra.")

    @commands.command()
    async def estado(self, ctx):
        await self.update_status_message()

async def setup(bot):
    # Aquí se pasa el canal ID como argumento
    await bot.add_cog(ServerStatus(bot, '1275593106967761058'))
