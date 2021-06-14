import discord
from discord.ext import commands
import nacl
import os
import requests
import random
import json
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncpraw

from MafZ import solve
from WebServer import StayAlive

import Moderation as md
import Utility as u
import Fun as f
#----------------------------------------------
intents = discord.Intents.default()
intents.members = True
#----------------------------------------------
#https://discord.com/oauth2/authorize?client_id=853591558493437982&scope=bot&permissions=8
intents = discord.Intents(messages=True, guilds=True)
client = commands.Bot(command_prefix="#", intents=intents)
owners = [564461721268518932, 433953456315957258]
reddit = asyncpraw.Reddit(
    client_id=os.getenv('RCID'),
    client_secret=os.getenv('RS'),
    user_agent="aggrobawt by vlad the not so glad",
)
#----------------------------------------------
not_good_words = [
    "nigga", "nigger", "Nigge", "simp", "faggot", "fag", "kaffir",
    "ching-chong"
]


@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name='#help and some sick music'))


@client.event
async def on_message(msg):
    try:
        await md.AntiSlur(msg, not_good_words, client)
    except:
        print("finally, inner peace")


@client.command()
async def hello(ctx):
    await ctx.send("Eyyyyyyyyy, what up m8?")


@client.command()
async def invite(ctx):
    await u.invite(ctx)


@client.command(aliases=['purge', 'p', 'c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
    await md.purge(ctx, amount)


@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason1="no reason"):
    await md.kick(ctx, member, reason1)


#@client.command()
#async def makemute(ctx,):


@client.command(aliases=['getmeme'])
async def meme(ctx):
    await f.getMeme(ctx, client, reddit)


@client.command(aliases=['ub'])
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx, *, member):
    await md.unban(ctx, member)


@client.command(aliases=['si', 'sinfo'])
async def serverinfo(ctx):
    await u.serverinfo(ctx)


@client.command()
async def whois(ctx, member: discord.Member):
    await u.whois(ctx, member)


@client.command(aliases=['dp', 'a'])
async def avatar(ctx, member: discord.Member = None):
    await u.avatar(ctx, member)


@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason="no reason"):
    await md.mute(ctx, member, reason)


@client.command()
async def setmute(ctx, role_id: int):
    json_file = open("ServMute.json", "r")
    role_ids = json.load(json_file)
    role_ids[ctx.guild.id] = role_id
    json_file.close()
    json_file = open("ServMute.json", "w")
    json.dump(role_ids, json_file)
    json_file.close()


@client.command(aliases=['b'])
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="no reason"):
    await md.ban(ctx, member, reason)


@client.command(aliases=['cf'])
async def coin(ctx):
    await u.coin(ctx)


@client.command()
async def roll(ctx, sides=6, startFromZero=False):
    await u.roll(ctx, sides, startFromZero)


@client.command()
async def eval(ctx, eqn=0):
    await u.eval(ctx, eqn)


@client.command()
async def joke(ctx, nsfw=False):
    await f.joke(ctx, nsfw)


@client.command()
async def gay(ctx, member: discord.Member):
    await f.gay(ctx, member)


@client.command()
async def createrole(ctx, *, content):
    guild = ctx.guild
    await guild.create_role(name=content)
    role = client.get(ctx.guild.roles, name='content')
    roleid = role.id
    description = f'''
    **Name:** <@{roleid}>
    **Created by:** {ctx.author.mention}
    '''
    embed = discord.Embed(name='New role created', description=description)
    await ctx.send(content=None, embed=embed)


#----------------------------------------------
StayAlive()
client.run(os.getenv("DiscordBotToken"))
