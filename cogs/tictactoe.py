import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
import copy

class TicTacToeGameView(discord.ui.View):
    
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.board : list = ["⬜" for _ in range(9)]
        self.saved_board : list = copy.deepcopy(self.board)
        self.turn : bool = True # True for X, False for O
        self.location_row : int = 0
        self.location_col : int = 0
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def reset_board(self):
        self.board = copy.deepcopy(self.saved_board)
        self.saved_board = copy.deepcopy(self.board)

    async def parse_board(self):
        return "".join(["".join(self.board[i - 3:i]) + "\n" for i in range(3,10,3)])

    async def edit_board(self, interaction):
        await self.reset_board()
        if self.board[(self.location_row * 3) + self.location_col] != "⬜":
            await interaction.response.send_message("Cannot place here, choose different place!", ephemeral=True, delete_after=3.0)
            return
        self.board[(self.location_row * 3) + self.location_col] = ":x:" if self.turn else ":o:"
        parsed_board = await self.parse_board()
        await self.message.edit(content=parsed_board, view=self)
    
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timedout")
        # await self.disable_all_items()

    @discord.ui.button(label="Row", 
                       style=discord.ButtonStyle.secondary,
                       disabled=True,
                       row=0)
    async def row_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="1",
                       style=discord.ButtonStyle.primary,
                       row=0)
    async def row_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_row = 0
        await self.edit_board(interaction)

    @discord.ui.button(label="2",
                       style=discord.ButtonStyle.primary,
                       row=0)
    async def row_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_row = 1
        await self.edit_board(interaction)

    @discord.ui.button(label="3",
                       style=discord.ButtonStyle.primary,
                       row=0)
    async def row_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_row = 2
        await self.edit_board(interaction)

    @discord.ui.button(label="Column", 
                       style=discord.ButtonStyle.secondary,
                       disabled=True,
                       row=1)
    async def column_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="1",
                       style=discord.ButtonStyle.primary,
                       row=1)
    async def col_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_col = 0
        await self.edit_board(interaction)
    
    @discord.ui.button(label="2",
                       style=discord.ButtonStyle.primary,
                       row=1)
    async def col_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_col = 1
        await self.edit_board(interaction)
    
    @discord.ui.button(label="3",
                       style=discord.ButtonStyle.primary,
                       row=1)
    async def col_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.location_col = 2
        await self.edit_board(interaction)

    @discord.ui.button(label="End Turn", 
                       style=discord.ButtonStyle.success,
                       row=4)
    async def end_turn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.turn = not self.turn
        self.saved_board = copy.deepcopy(self.board)
        if self.board.count("⬜") == 9:
            await interaction.response.send_message(f"Now it's {':x:' if self.turn else ':o:'}'s turn", view=self)
        else:
            await interaction.response.edit_message(content=f"Now it's {':x:' if self.turn else ':o:'}'s turn\n{await self.parse_board()}", view=self)
        # self.stop()

# Here we name the cog and create a new class for the cog.
class TicTacToe(commands.Cog, name="tictactoe"):

    def __init__(self, bot):
        self.bot = bot
        self.board = ["⬜" for _ in range(9)]

    @commands.hybrid_command(name="tictactoe",
                             description="Get a random fact.")
    @checks.not_blacklisted()
    async def tictactoe(self, ctx):
        view = TicTacToeGameView(timeout=50)
        # button = discord.ui.Button(label="Click me")
        # view.add_item(button)
        
        parsed_board = "".join(["".join(self.board[i - 3:i]) + "\n" for i in range(3,10,3)])

        message = await ctx.send(parsed_board, view=view)
        view.message = message
        
        await view.wait()
        # await view.disable_all_items()


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    pass
    await bot.add_cog(TicTacToe(bot))
