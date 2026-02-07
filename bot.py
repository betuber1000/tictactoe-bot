import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

games = {}

def print_board(board):
    return "\n".join([" | ".join(row) for row in board])

@bot.command()
async def tictactoe(ctx, opponent: discord.Member):
    if ctx.author.id in games or opponent.id in games:
        await ctx.send("Een van de spelers zit al in een spel!")
        return

    board = [["⬜" for _ in range(3)] for _ in range(3)]
    games[ctx.author.id] = {"board": board, "turn": ctx.author.id, "opponent": opponent.id}
    games[opponent.id] = games[ctx.author.id]
    await ctx.send(f"Tic Tac Toe gestart tussen {ctx.author.mention} en {opponent.mention}!\n{print_board(board)}\nHet is {ctx.author.mention} zijn beurt!")

@bot.command()
async def zet(ctx, rij: int, kolom: int):
    if ctx.author.id not in games:
        await ctx.send("Ur not in a game")
        return
    
    game = games[ctx.author.id]
    if ctx.author.id != game["turn"]:
        await ctx.send("Wait for your turn!")
        return
    
    board = game["board"]
    if board[rij][kolom] != "⬜":
        await ctx.send("taken")
        return
    
    board[rij][kolom] = "❌" if ctx.author.id == game["turn"] else "⭕"
    game["turn"] = game["opponent"] if ctx.author.id == game["turn"] else ctx.author.id
    await ctx.send(print_board(board))

bot.run("MTQ2OTc3MzE5MDM4NDMyMDYxNA.G5aEM5.47IRXGW8B59E1eE6m6aKUtVhdMbGTI4f3hYwMs")
