import discord
from discord.ext import commands
from discord.utils import get
import animec
import datetime
import praw
import requests
import json
import random
from PIL import Image,ImageFont,ImageDraw, ImageChops
from keep_alive import keep_alive
from io import BytesIO
import giphy_client
from giphy_client.rest import ApiException

TOKEN = 'your_bot_token'
ROLE = "Members"
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

bad_words = ["fuck", "nigga", "fuk", "cunt", "bitch", "dick", "d1ck", "pussy", "asshole", "bitch", "b!tch", "b1tch", "blowjob", "boobjob", "cock", "c0ck", "saale", "salle", "behenchod", "madarchod", "motherchod", "laudamal", "chodamal", "porn", "chutiye", "chutiya", "loda", "behen ke lode", "behenkelode", "harami", "haram khor", "haramkhor", "haram jade", "haramjade", "haram zade", "haramzade", "haram zada", "haramjada"]

invite = ["https://discord.com/invite/", "https://discord.gg/"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
]



reddit = praw.Reddit(
	client_id = "_zudj3PC0Rjx-vwh6HVilg", 
	client_secret = "0HH3CMum_dKpsNdJs9nXrhTm6f0ERg", 
	username = "BhupenSaini", 
	password = "tokyodrift30", 
	user_agent = "pythonpraw"
)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)



@client.event
async def on_ready():

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server. !help"))

    print('Logged in as {0.user}'.format(client))




@client.event
async def on_message(message):
    channel = client.get_channel(rulechannelid)
    msg = message.content
	

    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 2)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)
	

    for word in bad_words:
        if word in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} you are violating the rules. You just used a cuss word. \nIf you dont know the rules then go read the {channel.mention} channel.")
	
    for word in invite:
        if word in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} you are not allowed to send discord server invites. \nIf you dont know the rules then go read the {channel.mention} channel.")


    await client.process_commands(message)




@client.command()
async def help(ctx):
    fun = "!emojify <Yout Text>\n!gif <Your Text>\n!meme\n!quote"

    about = "!profile\n!serverinfo\n!avatar"

    anime = "!animechar <name of anime character>\n!anime <anime name>\n!aninews"

    level = "!level"
        
    embed = discord.Embed(
		title='Bhupen Saini Help Menu',
		description='This is a moderation bot. It is made using discord.py.\nPrefix of this bot is **!**. \n\n **The following are the commands:**',
		color=discord.Color.green()
		)
    embed.add_field(name='Fun', value=fun, inline=True)
    embed.add_field(name='About', value=about, inline=True)
    embed.add_field(name='Anime', value=anime, inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    await ctx.send(embed=embed)

@client.command()
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@client.command()
async def meme(ctx):
    subreddit = reddit.subreddit('memes')
        
    all_subs = []
    top = subreddit.top()

    for submission in top:
        all_subs.append(submission)
		
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url

    embed = discord.Embed(title = name)
    embed.set_image(url=url)

    await ctx.send(embed=embed)

@client.command()
async def anime(ctx, *, query):
	try:
		anime = animec.Anime(query)
	except:
		await ctx.send(embed = discord.Embed(description="No corresponding Anime is found for the search query.", color=discord.Color.red()))
		return

	embed = discord.Embed(
		title=anime.title_english,
		url=anime.url,
		description = f"{anime.description[:200]}...",
		color = random.choice(colors)
	)
	embed.add_field(name="Episodes", value=str(anime.episodes))
	embed.add_field(name="Rating", value=str(anime.rating))
	embed.add_field(name="Broadcast", value=str(anime.broadcast))
	embed.add_field(name="Status", value=str(anime.status))
	embed.add_field(name="Type", value=str(anime.type))
	embed.add_field(name="NSFW status", value=str(anime.is_nsfw()))
	embed.set_thumbnail(url=anime.poster)
	await ctx.send(embed=embed)


@client.command(aliases = ["char", "animecharacter"])
async def animechar(ctx,*,query):
	try:
		char = animec.Charsearch(query)
	except:
		await ctx.send(embed = discord.Embed(description="No corresponding Anime character is found for the search query.", color=discord.Color.red()))
		return
	
	embed = discord.Embed(
		title=char.title,
		url=char.url,
		color=random.choice(colors)
	)
	embed.set_image(url = char.image_url)
	embed.set_footer(text = ", ".join(list(char.references.keys())[:2]))
	await ctx.send(embed=embed)


@client.command()
async def aninews(ctx,amount:int=3):
	news = animec.Aninews(amount)

	links = news.links
	titles = news.titles
	descriptions = news.description

	embed = discord.Embed(title = "Latest Anime News", color=random.choice(colors), timestamp = datetime.datetime.utcnow())
	embed.set_thumbnail(url = news.images[0])

	for i in range(amount):
		embed.add_field(name=f"{i+1} {titles[i]}", value=f"{descriptions[i][:200]}...\n[Read more({links[i]})]",inline=False)
		
	await ctx.send(embed=embed)



@client.command()
async def emojify(ctx, *, text):
	emojis = []
	for s in text.lower():
		if s.isdecimal():
			num2emo = {'0':'zero', '1':'one', '2':'two', '3':'three',
						'4':'four','5':'six','7':'seven','8':'eight','9':'nine'}
			emojis.append(f':{num2emo.get(s)}:')
		elif s.isalpha():
			emojis.append(f':regional_indicator_{s}:')
		else:
			emojis.append(s)
	
	await ctx.send(''.join(emojis))


@client.command(aliases=['m'])
async def mute(ctx, member: discord.Member):
	muted_role = ctx.guild.get_role(yourmutedroleid)

	await member.add_roles(muted_role)

	await ctx.send(member.mention + " has been muted")




@client.command()
async def profile(ctx, member:discord.Member=None):

    if not member:
        member = ctx.author
		
    name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()

    created_at = member.created_at.strftime(f"%a %b\n%B %Y")
    joined_at = member.joined_at.strftime(f"%a %b\n%B %Y")
		
    money,level = "NULL", "NULL"
        
    base = Image.open("base.png").convert("RGBA")
    background = Image.open("bg.png").convert("RGBA")

    pfp = member.avatar_url_as(size=256)
    data = BytesIO(await pfp.read())
    pfp = Image.open(data).convert("RGBA")

    name = f"{name[:16]}.." if len(name)>16 else name
    nick = f"AKA - {nick[:17]}.." if len(nick)>17 else f"AKA - {nick}"
    draw = ImageDraw.Draw(base)
    pfp = circle(pfp, size=(215,215))
    font = ImageFont.truetype("arial.ttf",38)
    akafont = ImageFont.truetype("arial.ttf",30)
    subfont = ImageFont.truetype("arial.ttf",25)
        
    draw.text((280,240),name,font=font)
    draw.text((270,315),nick,font=akafont)
    draw.text((65,490),Id,font=subfont)
    draw.text((405,490),status,font=subfont)
    draw.text((65,635),money,font=subfont)
    draw.text((405,635),level,font=subfont)
    draw.text((65,770),created_at,font=subfont)
    draw.text((405,770),joined_at,font=subfont)

    base.paste(pfp,(56,158), pfp)
    background.paste(base, (0,0), base)

    with BytesIO() as a:
        background.save(a, "PNG")
        a.seek(0)
        await ctx.send(file=discord.File(a,"pro.png"))


@client.command()
async def avatar(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar_url


    avaEmbed = discord.Embed(title=f"{member.name}'s Avatar")
    avaEmbed.set_image(url=memberAvatar)
    await ctx.send(embed=avaEmbed)


@client.command()
async def gif(ctx,*,q="smile"):
	api_key = 'yourapikey'
	api_instance = giphy_client.DefaultApi()

	try:
		api_responce = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
		lst = list(api_responce.data)
		giff = random.choice(lst)

		embed = discord.Embed()
		embed.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

		await ctx.send(embed=embed)
	
	except ApiException as e:
		print("Exception when calling API")



@client.command()
async def serverinfo(ctx):
    guild = client.get_guild(youserverid)
        
    name = str(guild.name)
    description = str(guild.description)

    owner = str(guild.owner)
    region = str(guild.region)
    memberCount = str(guild.member_count)
    icon = str(guild.icon_url)
		
    embed = discord.Embed(
		title = "Server Info",
		description = description,
		color = discord.Color.blue(),
	)

    embed.set_thumbnail(url=icon)
    embed.add_field(name='Owner', value=owner, inline=True)
    embed.add_field(name='Region', value=region, inline=True)
    embed.add_field(name='Member Count', value=memberCount, inline=True)

    await ctx.send(embed=embed)


def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

@client.event
async def on_member_join(member):
    guild = client.get_guild(youserverid)
    channel = guild.get_channel(welcomechannelid)
    channell = guild.get_channel(rulechannelid)


    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


    await member.send(f'welcome {member.mention}:partying_face:! Pls check the #{channell.mention} channel. \nHope you enjoy your time here.')

    role = get(member.guild.roles, name=ROLE)
    await member.add_roles(role)

    welcome = Image.open("wp.jpg")
    font = ImageFont.truetype("arial.ttf", 200)
    draw = ImageDraw.Draw(welcome)
    text = f"Welcome to the Hub!\n\nMember Count:  {get_guild_member_count(guild)}"
    draw.text((1062,1426), text, (255,255,255), font=font)

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((1076,1076))
    
    welcome.paste(pfp, (1405,203))
    welcome.save("profile.jpg")
    await channel.send(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n:partying_face: Hey {member.mention}, welcome to the server! :partying_face: \n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{member.mention} Please go through #{channell.mention} before you go ahead! \n\nEnjoy yout time, stay here and have fun.\n\nThanks for joining!")
    await channel.send(file=discord.File("profile.jpg"))


@client.command()
async def level(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        xp =  users[str(id)]['experience']
        await ctx.send(f'You are at level {lvl}! {member.name}')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')
		

def get_guild_member_count(guild):
	return len(guild.members)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

keep_alive()
client.run(TOKEN)
