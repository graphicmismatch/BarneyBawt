import discord
from discord.ext import commands
import nacl
import os
import requests
import random
import json
import urllib.request


async def purge(ctx, amt):
    amt += 1
    await ctx.channel.purge(limit=amt)
    await ctx.send(f"Deleted {amt-1} message(s)!")


async def kick(ctx, member: discord.Member, reason="no reason"):
    await ctx.send(f"{member.mention} has been kicked for {reason}")
    try:
        await member.send("you have been kicked from the server")
    except:
        await ctx.send("Member could not be direct messaged.")
    await member.kick(reason=reason)


async def ban(ctx, member: discord.Member, reason="no reason"):
    await ctx.send(f"{member.mention} has been banned for {reason}")
    try:
        await member.send("you have been banned from the server")
    except:
        await ctx.send("Member could not be direct messaged.")
    await member.ban(reason=reason)


async def unban(ctx, member):
    banned_members = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_members:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned!!")
            return
    await ctx.send("member not found")


async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    muterole = discord.utils.get(guild.roles, name="Mute")
    await member.remove_roles(muterole)
    await ctx.send(member.mention + " has been unmuted")


async def mute(ctx, member: discord.Member, reason="no reason"):
    guild = ctx.guild
    muterole = discord.utils.get(guild.roles, name="Mute")

    if not muterole:
        muterole = await guild.create_role(name="Mute")

        for channel in guild.channels:
            await channel.set_permissions(muterole,
                                          speak=False,
                                          send_messages=False,
                                          read_messages=True,
                                          read_message_history=True)

    await member.add_roles(muterole, reason=reason)
    await ctx.send(
        f"{member} has been muted for{reason} by {ctx.message.author}")


async def AntiSlur(msg, not_good_words, client):
    for words in not_good_words:
        if words.casefold() in msg.content.casefold():
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention}  dont swear!!")

        if ":" == msg.content[0] and ":" == msg.content[-1]:
            emo_name = msg.content[1:-1]
            for emoji in msg.guild.emojis:
                if emo_name == emoji.name:
                    try:
                        await msg.channel.send(str(emoji))
                        await msg.delete()
                    except IndexError:
                        print("not an emoji")

                    break
    await client.process_commands(msg)
