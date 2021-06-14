import discord
from discord.ext import commands
import nacl
import os
import requests
import random
import json
import urllib.request

from MafZ import solve


async def invite(ctx):
    await ctx.send("https://bit.ly/BarneyBawt")


async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=discord.Color.random())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="members", value=ctx.guild.member_count)
    embed.add_field(name="ID", value=ctx.guild.id)
    embed.add_field(name="region", value=ctx.guild.region)
    embed.add_field(name="owner", value=ctx.guild.owner)
    await ctx.send(embed=embed)


async def whois(ctx, member: discord.Member):
    roles = [role for role in member.roles]
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"{member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="name", value=member.display_name, inline=True)
    embed.add_field(
        name="created at:",
        value=member.created_at.strftime("%a, %#d %B %Y, %I : %M %p UTC"),
        inline=True)
    embed.add_field(
        name="joined at:",
        value=member.joined_at.strftime("%a, %#d %B %Y, %I : %M %p UTC"),
        inline=True)

    embed.add_field(name="top role",
                    value=member.top_role.mention,
                    inline=True)
    embed.add_field(name="Bot?", value=member.bot, inline=True)
    embed.add_field(name="Roles",
                    value=" ".join(role.mention for role in roles),
                    inline=True)
    await ctx.send(embed=embed)


async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    avatar = member.avatar_url
    embed = discord.Embed(title=member.name, color=discord.Colour.random())
    embed.add_field(name="animated?", value=member.is_avatar_animated())

    embed.set_image(url=avatar)

    await ctx.send(embed=embed)


async def eval(ctx, eqn=0):
    await ctx.send(f"The answer is:\n**{solve(eqn)}**")


async def coin(ctx):
    x = random.randint(1, 2)
    ht = "heads" if x % 2 == 0 else "tails"
    await ctx.send(f"A coin was flipped...**{ht.upper()}**!")


async def roll(ctx, sides=6, startFromZero=False):
    x = random.randint(1, sides)
    if startFromZero:
        x -= 1
    await ctx.send(f"The die rolled a **{x}**!")
