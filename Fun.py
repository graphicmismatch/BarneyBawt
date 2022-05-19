import discord
import nacl
import os
import random
import aiohttp
import re
import urllib.request
import math;
import requests
import json

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


async def ytsrch(ctx, srchTerm):
    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + srchTerm)
    videoIds = re.findall(r"/watch\?v=(\S{11})", html.read().decode())
    await ctx.send(f"Here is the link (father, kill me):\n\nhttps://youtu.be/{videoIds[0]}")


async def getMeme(ctx):
    embed = discord.Embed(color=discord.Colour.random())
    res = "";
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
        res = await r.json()
    e = res['data']['children'][random.randint(0, 25)]
    embed.title = e['data']['title']
    embed.set_image(url=e['data']['url'])
    embed.set_footer(
      text=
      "mememememememememememememememememememememememememememememe"
     )
    await ctx.channel.send(embed=embed)

async def getPost(ctx, reddit, sub):
  sub = await reddit.subreddit(sub, fetch=True)
  posts = sub.hot(limit=100)
  submission = []
  async for item in posts:
      submission.append(item)
  e = submission[random.randint(0, 100)]
  embed = discord.Embed(title=e.title, url=e.url, color=discord.Colour.random())
  embed.set_image(url=e.url)
  embed.set_footer(
      text=
      f"Post from r/{sub} from reddit.com... you're too lazy to go there anyways"
  )
  await ctx.send(embed=embed)




async def getLyrics(ctx, term, isUn, sp, genius):
    t = ""
    if not isUn:
        x = [
            "(Remix)", "(Live)", "Remix", "Live", "(Remastered)", "Remastered"
        ]
        term = term.replace(" ", "+")
        t = sp.search(q=term, type='track')["tracks"]["items"][0]["name"]
        for n in x:
            t = t.replace(n, "")
        t = t.strip()
        song = (genius.search_song(
            t,
            sp.search(q=term, type='track')["tracks"]["items"][0]["album"]
            ["artists"][0]["name"]))
    else:
        song = (genius.search_song(term))
    print(song)
    try:
        lyrics = song.lyrics
        print(lyrics)
        artist = sp.search(
            q=term,
            type='track')["tracks"]["items"][0]["album"]["artists"][0]["name"]
        lyrics = lyrics.replace("EmbedShare URLCopyEmbedCopy", "")
        msg =  str(
            f"**{t} by {artist}:**\n\n{lyrics}\n\n\nData from Genius.com")
        msgs = splitMessage(msg)
        for m in msgs:
          await ctx.send(m)
    except:
        await ctx.send(song)


async def getSpotifyLink(ctx,term,sp):
  try:
    term = term.replace(" ", "+")
    id = sp.search(q=term, type='track')["tracks"]["items"][0]["id"]
    await ctx.send( f"https://open.spotify.com/track/{id}")
  except:
    await ctx.send(f"nope, nothing")


def getTrackIds(pid,sp):
    results = sp.user_playlist_tracks("1p557z5v30ztwmn0oolyiln6t",
                                      pid)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    idList = []
    for i in range(len(tracks) - 1):
        idList.append(tracks[i]["track"]["id"])
    return idList


async def getTopTen(ctx,sp):
    musicNameList = []
    musicArtistList = []
    i = -1
    playlist = sp.playlist(os.getenv('TTPID'))
    for item in playlist["tracks"]["items"]:
        i += 1
        music_track = item["track"]
        musicNameList.append(music_track["name"])
        meta = sp.track(music_track["id"])
        musicArtistList.append(meta["album"]["artists"][0]["name"])
    lis = "(Data from Spotify Top 50 playlist)\n\nHahaha never send a pathetic human to do a robots job. By the way, here are the top ten songs today:\n\n"
    for nam in range(10):
        lis += f"{(nam+1)}. {musicNameList[nam]} ~{musicArtistList[nam]}\n"
    await ctx.send(lis)


async def getTrack(ctx,sp):
    playlist = os.getenv('PID')
    track_ids =  getTrackIds(playlist,sp)
    l = len(track_ids)
    l -= 1
    trackNo = round(random.random() * l)
    await ctx.send( "Once amore, the puny humans require my assistance. Well, here is the song:\n\nhttps://open.spotify.com/track/" + track_ids[
        trackNo])

async def getPickupLine(ctx):
  x = requests.request("GET","https://getpickuplines.herokuapp.com/lines/random")
  request = json.loads(x.text)
  line = request["line"]
  await ctx.send(f"Here iz pick up line for u: \n  {line}")
  

def splitMessage(s):
    m = []
    if len(s) <= 2000:
        m.append(s)
        return m
    else:
        s += "m"
        for i in range(math.ceil(len(s) / 2000)):
            m.append(s[(i) *
                       2000:(((i + 1) *
                              2000) if len(s) >= ((i + 1) * 2000) else -1)])
        return m
