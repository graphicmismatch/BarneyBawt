import discord
from discord.ext import commands
import nacl
import os
import requests
import random
import json
import urllib.request

from dadjokes import Dadjoke
from jokeapi import Jokes


async def joke(ctx, nsfw=False):
    if random.randint(0, 1) % 2 == 0:
        dadjoke = Dadjoke()
        joke = dadjoke.joke + "\n\nSomeone kill me for this."
        await ctx.send(joke)
    else:
        try:
            j = Jokes()
            if nsfw:
                joke = j.get_joke(blacklist=[], lang="en")
            else:
                joke = j.get_joke(
                    blacklist=['nsfw', 'racist', 'sexist', 'religious'],
                    lang="en")
            if joke["type"] == "single":
                await ctx.send(joke["joke"] + "\n\nSomeone kill me for this")
            else:
                await ctx.send(joke["setup"] + "\n\n\n" + joke["delivery"] +
                               "\n\nSomeone kill me for this")
        except:
            dadjoke = Dadjoke()
            joke = dadjoke.joke + "\n\nSomeone kill me for this."
            await ctx.send(joke)


async def gay(ctx, member: discord.Member):
    embed = discord.Embed(color=discord.Colour.random())
    embed.title = "Gay meter"
    embed.description = f'{member.mention} is {random.randint(1, 100)}% Gay'
    await ctx.send(embed=embed)


async def getMeme(ctx, client, reddit):
    memesub = await reddit.subreddit("memes", fetch=True)
    memes = memesub.hot(limit=100)
    submission = []
    async for item in memes:
        submission.append(item)
    e = submission[random.randint(0, 100)]
    embed = discord.Embed(title=e.title, url=e.url, color=0x109319)
    embed.set_image(url=e.url)
    embed.set_footer(
        text=
        "Meme from r/memes from reddit.com... you're too lazy to go there anyways"
    )
    await ctx.send(embed=embed)
