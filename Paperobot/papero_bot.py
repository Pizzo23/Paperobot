import discord
from discord.ext import commands
import random
import logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Il bot è connesso come {bot.user}')

wallets = {}

def get_balance(user_id):
    return wallets.get(user_id, 100)

def update_balance(user_id, amount):
    wallets[user_id] = get_balance(user_id) + amount

@bot.command()
async def saldo(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f"💰 Hai {balance} papere.")

@bot.command()
async def dadi(ctx, scommessa: int):
    if get_balance(ctx.author.id) < scommessa or scommessa <= 0:
        await ctx.send("❌ Scommessa non valida.")
        return

    player = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    await ctx.send(f"🎲 Hai tirato {player}, io ho tirato {bot_roll}.")

    if player > bot_roll:
        update_balance(ctx.author.id, scommessa)
        await ctx.send(f"Hai vinto! 🐥 +{scommessa} papere.")
    elif player < bot_roll:
        update_balance(ctx.author.id, -scommessa)
        await ctx.send(f"Hai perso! 🐥 -{scommessa} papere.")
    else:
        await ctx.send("Pareggio! Nessuna papera persa o guadagnata.")

@bot.command()
async def blackjack(ctx, scommessa: int):
    if get_balance(ctx.author.id) < scommessa or scommessa <= 0:
        await ctx.send("❌ Scommessa non valida.")
        return

    player = random.randint(15, 21)
    dealer = random.randint(17, 23)

    await ctx.send(f"🃏 Hai fatto {player}, il banco ha {dealer}.")

    if player > 21:
        outcome = -scommessa
        msg = "Hai sballato! ❌"
    elif dealer > 21 or player > dealer:
        outcome = scommessa
        msg = f"Hai vinto! 🥳 +{scommessa} papere."
    elif player == dealer:
        outcome = 0
        msg = "Pareggio!"
    else:
        outcome = -scommessa
        msg = f"Hai perso! 😢 -{scommessa} papere."

    update_balance(ctx.author.id, outcome)
    await ctx.send(msg)

bot.run('MTM5OTYxNjkyOTY4NTMwNzM5Mg.GKw3MV.A9zvlgSCBhgB90M6sDgc9cAHj4umrTTFbAxGYk')
