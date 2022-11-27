import discord;
from discord.ext import commands;
import nacl;
import os;
import random;
import json;
import spotipy;
from spotipy.oauth2 import SpotifyClientCredentials;
import asyncpraw;
from os import system;
from WebServer import StayAlive;

import lyricsgenius as lg;
import Moderation as md;
import Utility as u;
import Fun as f;
#----------------------------------------------
intents = discord.Intents.default();
intents.members = True;
#----------------------------------------------
#https://discord.com/oauth2/authorize?client_id=853591558493437982&scope=bot&permissions=8;
intents = discord.Intents(messages=True, guilds=True);
client = commands.Bot(command_prefix="#", intents=intents);
owners = [564461721268518932, 433953456315957258];
reddit = asyncpraw.Reddit(
    client_id=os.getenv('RCID'),
    client_secret=os.getenv('RS'),
    user_agent="BarneyBawt by Vlad the not so Glad and BenderLLL",
);
#----------------------------------------------
not_good_words = ["nigger"];

emojis = ["🇺", "💥", "🇬", "🇦", "🇾"];
pongreactions = ["Wtf m8", "Why?", "Dipshit", "Wtf", "Y PONG?", "Kill me"];
#----------------------------------------------
spotify_client_credentials = SpotifyClientCredentials(os.getenv('SPOTCLIID'),
                                                      os.getenv('SPOTSECRET'));
auth_manager = spotify_client_credentials;
sp = spotipy.Spotify(auth_manager=auth_manager);
#----------------------------------------------
genius = lg.Genius(os.getenv('GENIUSKEY'),
                   skip_non_songs=True,
                   excluded_terms=[
                       "(Remix)", "(Live)", "Remix", "Live", "(Remastered)",
                       "(Live)", "Remastered", "Live"
                   ],
                   remove_section_headers=True);


@client.event
async def on_ready():
	print(f"logged in as {client.user}");
	await client.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.listening, name='#help and some sick music'));


@client.event
async def on_message(ctx):
	if "hi bot" in ctx.content.lower():
		await ctx.channel.send("Hello " + ctx.author.mention + " \n y pong");
	if "@everyone" in ctx.content or "@here" in ctx.content:
		for emo in emojis:
			print(emo);
			await ctx.add_reaction(emo);
		await ctx.channel.send(pongreactions[random.randint(
		    0,
		    len(pongreactions) - 1)]);
	if "or am i" in ctx.content.lower() or "or is it" in ctx.content.lower():
		await ctx.channel.send("https://youtu.be/1dwu4iVA1yo");
	await md.AntiSlur(ctx, not_good_words, client);
	await u.EmojiGiver(ctx);
	await client.process_commands(ctx);


@client.command()
async def hello(ctx):
	await ctx.send("Eyyyyyyyyy, what up m8?");


@client.command()
async def invite(ctx):
	await u.invite(ctx);


@client.command(aliases=['yt', 'youtube', 'youtubesearch'])
async def ytsrch(ctx, srchTerm):
	srchTerm = (ctx.message.content)[ctx.message.content.index(" "):];
	srchTerm = srchTerm.replace(" ", "+");
	await f.ytsrch(ctx, srchTerm);


@client.command(aliases=['post', 'redditpost', 'sub'])
async def getpost(ctx, srchTerm):
	srchTerm = (ctx.message.content)[ctx.message.content.index(" "):];
	srchTerm = srchTerm.replace(" ", "+");
	await f.getPost(ctx, reddit, srchTerm);


@client.command(aliases=['purge', 'p', 'c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
	await md.purge(ctx, amount);


@client.command(aliases=['adpurge', 'adp', 'adc'])
async def adclear(ctx, amount=1):
	if str(ctx.author.id) == "433953456315957258" or str(
	    ctx.author.id) == "899664285561663518":
		await md.purge(ctx, amount);


@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason1="no reason"):
	await md.kick(ctx, member, reason1);


#@client.command()
#async def makemute(ctx,):


@client.command(aliases=['getmeme'])
async def meme(ctx):
	await f.getMeme(ctx);


@client.command(aliases=['ub'])
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx, *, member):
	await md.unban(ctx, member);


@client.command(aliases=['si', 'sinfo'])
async def serverinfo(ctx):
	await u.serverinfo(ctx);


@client.command()
async def whois(ctx, member: discord.Member):
	await u.whois(ctx, member);


@client.command(aliases=['dp', 'a'])
async def avatar(ctx, member: discord.Member = None):
	await u.avatar(ctx, member);


@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason="no reason"):
	await md.mute(ctx, member, reason);


@client.command()
async def setmute(ctx, role_id: int):
	json_file = open("ServMute.json", "r");
	role_ids = json.load(json_file);
	role_ids[ctx.guild.id] = role_id;
	json_file.close();
	json_file = open("ServMute.json", "w");
	json.dump(role_ids, json_file);
	json_file.close();


@client.command(aliases=['b'])
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="no reason"):
	await md.ban(ctx, member, reason);


@client.command(aliases=['cf'])
async def coin(ctx):
	await u.coin(ctx);


@client.command(aliases=['spsrch'])
async def spotifysearch(ctx, term):
	term = (ctx.message.content)[ctx.message.content.index(" "):]
	await f.getSpotifyLink(ctx, term, sp);


@client.command(aliases=['recsong'])
async def songrec(ctx):
	await f.getTrack(ctx, sp);


@client.command(aliases=['lyrics'])
async def songlyrics(ctx):
	term = ""
	isun = False
	if "," in ctx.message.content:
		term = (ctx.message.content)[ctx.message.content.index(" "):ctx.
		                             message.content.index(",")];
		isun = (ctx.message.content)[ctx.message.content.index(","):];
	else:
		term = (ctx.message.content)[ctx.message.content.index(" "):];
		isun = False;
	await f.getLyrics(ctx, term, isun, sp, genius);


@client.command(aliases=['tt'])
async def topten(ctx):
	await f.getTopTen(ctx, sp);


@client.command()
async def roll(ctx, sides=6, startFromZero=False):
	await u.roll(ctx, sides, startFromZero);


@client.command()
async def eval(ctx):
	eqn = ctx.message.content[ctx.message.content.index(" "):]
	await u.eval(ctx, eqn);


@client.command()
async def joke(ctx, nsfw=False):
	await f.joke(ctx, nsfw);

@client.command()
async def gay(ctx, member: discord.Member):
	await f.gay(ctx, member);
	

@client.command(aliases=['pu', 'pul', 'line', 'pickup'])
async def pickupline(ctx):
	await f.getPickupLine(ctx);


@client.command()
async def createrole(ctx, *, content):
	guild = ctx.guild;
	await guild.create_role(name=content);
	role = client.get(ctx.guild.roles, name='content');
	roleid = role.id;
	description = f'''
    **Name:** <@{roleid}>
    **Created by:** {ctx.author.mention}
    ''';
	embed = discord.Embed(name='New role created', description=description);
	await ctx.send(content=None, embed=embed);


#----------------------------------------------
StayAlive();

#try:
client.run(os.getenv("DiscordBotToken"));
#except discord.errors.HTTPException:
	#print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
	#system("python restarter.py")
	#system('kill 1')
