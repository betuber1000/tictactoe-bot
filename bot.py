import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Active games
games = {}

def print_board(board):
    return "\n".join([" | ".join(row) for row in board])

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "⬜":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "⬜":
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "⬜":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "⬜":
        return board[0][2]
    # Check tie
    if all(cell != "⬜" for row in board for cell in row):
        return "Tie"
    return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# Start a new game
@bot.tree.command(name="tictactoe", description="Start a Tic Tac Toe game")
@app_commands.describe(opponent="Select your opponent")
async def tictactoe(interaction: discord.Interaction, opponent: discord.Member):
    if interaction.user.id in games or opponent.id in games:
        await interaction.response.send_message("One of the players is already in a game!", ephemeral=True)
        return

    board = [["⬜" for _ in range(3)] for _ in range(3)]
    games[interaction.user.id] = {"board": board, "turn": interaction.user.id, "opponent": opponent.id}
    games[opponent.id] = games[interaction.user.id]
    await interaction.response.send_message(
        f"Tic Tac Toe started between {interaction.user.mention} and {opponent.mention}!\n"
        f"{print_board(board)}\nIt is {interaction.user.mention}'s turn!"
    )

# Make a move
@bot.tree.command(name="move", description="Place your X or O on the board")
@app_commands.describe(row="Row number (0-2)", column="Column number (0-2)")
async def move(interaction: discord.Interaction, row: int, column: int):
    if interaction.user.id not in games:
        await interaction.response.send_message("You are not in a game!", ephemeral=True)
        return

    game = games[interaction.user.id]
    if interaction.user.id != game["turn"]:
        await interaction.response.send_message("It's not your turn!", ephemeral=True)
        return

    board = game["board"]
    if board[row][column] != "⬜":
        await interaction.response.send_message("This cell is already taken!", ephemeral=True)
        return

    mark = "❌" if interaction.user.id == game["turn"] else "⭕"
    board[row][column] = mark

    winner = check_winner(board)
    if winner:
        if winner == "Tie":
            msg = f"It's a tie!\n{print_board(board)}"
        else:
            msg = f"{interaction.user.mention} wins!\n{print_board(board)}"
        # Remove game
        del games[interaction.user.id]
        del games[game["opponent"]]
        await interaction.response.send_message(msg)
        return

    # Switch turn
    game["turn"] = game["opponent"] if interaction.user.id == game["turn"] else interaction.user.id
    await interaction.response.send_message(f"{print_board(board)}\nIt is now <@{game['turn']}>'s turn!")

# Run bot with token from environment variable
bot.run(os.environ['DISCORD_TOKEN'])
