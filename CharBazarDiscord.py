from io import StringIO
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from SearchAuctionsSrapper import search_auctions
from functools import reduce

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
Intent = discord.Intents.default()
Intent.message_content = True
Bot = commands.Bot(command_prefix='.', intents=Intent)

def format_message(accumulator, auction):
    name = auction['name']
    bid = auction['bid']
    link = auction['link']
    features = reduce(lambda acc, feature : acc + f'{feature} \n', auction['features'], '')
    char_info = f'**Name:** {name}\n**Value:** {bid} TC\n**Link: **{link}\n**Features:**\n{features}'
    return accumulator + char_info + '\n'

@Bot.command(name='bazar')
async def find_in_bazar(ctx, *args):
    world = args[args.index("$world") + 1]
    vocation = args[args.index('$vocation') + 1]
    await ctx.send(f'Searching on world: {world} with vocation: {vocation} for ending soon bids')

    auctions = search_auctions(world, vocation)
    message = reduce(format_message, auctions, '')

    if len(message) > 2000:
        buffer = StringIO(message)
        f = discord.File(buffer, filename='char-bazar.txt')
        await ctx.send(file=f)
    elif len(message) == 0:
        await ctx.send(f'No ending bids available in {world} with vocation {vocation}')
    else:
        await ctx.send(message)

Bot.run(TOKEN)