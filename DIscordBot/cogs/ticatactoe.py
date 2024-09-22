import discord
from discord.ext import commands
from discord import app_commands
from typing import List

class TicTacToeButton(discord.ui.Button):
    def __init__(self, x, y):
        super().__init__(label="\u200b", style=discord.ButtonStyle.secondary, row=x)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if self in view.disabled_buttons:
            return await interaction.response.send_message("¡No puedes usar este botón!", ephemeral=True)
        
        if view.current_player == interaction.user:
            if view.board[self.x][self.y] in ('X', 'O'):
                return await interaction.response.send_message("¡Movimiento no válido!", ephemeral=True)
            view.board[self.x][self.y] = view.current_player_symbol
            self.style = discord.ButtonStyle.success if view.current_player_symbol == 'X' else discord.ButtonStyle.danger
            self.label = view.current_player_symbol
            self.disabled = True
            view.disabled_buttons.append(self)
            view.update_board()
            winner = view.check_winner()
            if winner:
                view.disable_all_buttons()
                await interaction.response.edit_message(content=f"¡{view.current_player.mention} ha ganado!", view=view)
                view.stop()
            elif all(view.board[i][j] in ('X', 'O') for i in range(3) for j in range(3)):
                view.disable_all_buttons()
                await interaction.response.edit_message(content="¡Es un empate!", view=view)
                view.stop()
            else:
                view.current_player, view.current_player_symbol = (view.player2, 'O') if view.current_player == view.player1 else (view.player1, 'X')
                await interaction.response.edit_message(content=f"Es el turno de {view.current_player.mention}", view=view)
        else:
            await interaction.response.send_message("¡No es tu turno!", ephemeral=True)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.current_player_symbol = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.disabled_buttons = []

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def update_board(self):
        for child in self.children:
            if self.board[child.x][child.y] == 'X':
                child.style = discord.ButtonStyle.success
                child.label = 'X'
            elif self.board[child.x][child.y] == 'O':
                child.style = discord.ButtonStyle.danger
                child.label = 'O'

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] in ('X', 'O'):
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] in ('X', 'O'):
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] in ('X', 'O'):
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] in ('X', 'O'):
            return self.board[0][2]
        return None

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True

class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="3enraya", description="Inicia un duelo a muerte de 3 en raya ☠")
    async def _3enraya(self, interaction: discord.Interaction, oponente: discord.Member):
        if interaction.user == oponente:
            await interaction.response.send_message("No puedes jugar contra ti mismo.", ephemeral=True)
            return
        view = TicTacToe(interaction.user, oponente)
        await interaction.response.send_message(f"Es el turno de {interaction.user.mention}", view=view)

async def setup(bot):
    await bot.add_cog(TicTacToeCog(bot))

# Asegúrate de que el archivo se guarda como 'ticatactoe.py' y está en el directorio 'cogs'.
