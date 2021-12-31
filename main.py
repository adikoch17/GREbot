import os
import discord
from discord.ext import commands
from replit import db
from collections import OrderedDict
import datetime
from tabulate import tabulate
import asyncio
import random
from keep_alive import keep_alive
from pretty_help import DefaultMenu, PrettyHelp

my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())

# bot.remove_command("help")

client = discord.Client()

try:
  score=db["score"]
  prizes = db["prizes"]
except:
  db["score"]={}
  score = db["score"].value
  db["prizes"] = []
  prizes = db["prizes"].value

  
async def reset():
  await bot.wait_until_ready()
  ch =  bot.get_channel(925799445281509386)
  while(True):
    msg_sent =False
    x = datetime.datetime.now()
    if int(x.strftime("%M"))==0:
      if int(x.strftime("%H"))==0:
        if int(x.strftime("%w"))==2 and not msg_sent:
          db["score"]={}
          score = {}
          print("mesg sent")
          await ch.send("**Resetting scores** :cd: :hammer:")
          msg_sent = True
    else:
      msg_sent=False
    await asyncio.sleep(60)

async def announce_winners():
  await bot.wait_until_ready()
  ch =  bot.get_channel(925799445281509386)
  while(True):
    msg_sent =False
    x = datetime.datetime.now()
    if int(x.strftime("%w"))==1 and not msg_sent:
      D1 = OrderedDict(sorted(score.items(), key = lambda t: t[1],reverse=True))
      D1= D1.items()
      winner = f" |       |\n(| {D1[0][0][0:5]} |)\n |  #X   |\n  \     /\n   `---'\n   _|_|_\n"
      allowed_mentions = discord.AllowedMentions(everyone = True)
      await ch.send(content = "@everyone **the results are here!** ", allowed_mentions = allowed_mentions)
      await ch.send("https://tenor.com/view/excited-so-drums-gif-11982656")
      await ch.send("**And the winner is**")   
      await ch.send("```\n"+winner+"\n```")
      await ch.send(f"Congratulation **{D1[0][0]}!** you have won: **{random.choice(db['prizes'].value)}**")
      await ch.send("**PA:You can now suggest prize ideas, ideas will be accepted until midnight**")
      await asyncio.sleep(3600*24)
    else:
      msg_sent=False
    await asyncio.sleep(3600)

  


@bot.event
async def on_ready():
    ch =  bot.get_channel(925799445281509386)
    print("The bot has intialized..")
    await ch.send("I AM ALIVE\nGREbot is a discord bot to gamify our GRE prep process. Every day you input the number of hours you spend studying.Your points are calculated and stored for you to view.At the end of the week, you get a report of who is in lead. This person is also the winner for the week and will get a prize.For example, a prize could be a pack of Oreos, or maybe cup noodles or admin rights for the server. It can be decided on a weekly basis.\n\nUsage :-\n**$studied 5** # letting the bot know you studied for 5 hrs\n**$leaderboard** # show the leaderboard of the week\n**$prize shwarma**# Adding the prize of 'shwarma' to the pot\n**$show_prizes** #show the prizes you might win at the end of the week\n**$hlp** # show the usage\n")
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
              return
    if message.content.startswith('$helloooo'):
        await message.channel.send('Hellooo!')
    await bot.process_commands(message)
    
@bot.command()
async def ping(ctx, arg):
    await ctx.send(f"{ctx.message.author} "+arg)
    print(db["score"].value)

@bot.command()
async def studied(ctx,arg):
    x = datetime.datetime.now()
    if int(x.strftime("%w"))!=1:
      try:
        curr_scr = score[f"{ctx.message.author}"]
        new_scr = int(curr_scr)+int(arg)
        score[f"{ctx.message.author}"] = new_scr
        print("try")
      except:
        score[f"{ctx.message.author}"] = int(arg)
        print("except")
      db["score"] = score
    else:
      ctx.send("Today is result day! no entries will be accepted :p")


@bot.command()
async def leaderboard(ctx):
    x = datetime.datetime.now()
    if int(x.strftime("%w"))!=1: 
      score = db["score"].value
      if not bool(score):
        await ctx.send("No participants for this week yet :slight_frown: ")
      else:
        D1 = OrderedDict(sorted(score.items(), key = lambda t: t[1],reverse=True))
        print(D1)
        s= tabulate(D1.items(),["Player","Score"],tablefmt="grid")
        print(s)
        await ctx.send("``` \n"+s+"```")
    else:
      await ctx.send("Today is result day! no leaderboard today :p")

@bot.command()
async def prize(ctx,arg):
  x = datetime.datetime.now()
  if int(x.strftime("%w"))==1:
    prizes = db["prizes"]
    prizes.append(arg)
    db["prizes"] = prizes
  else:
    await ctx.send("Sorry! not accepting ideas right now! You can suggest prizes on result day(Monday)")

@bot.command()
async def help(ctx):
  hlp = "GREbot is a discord bot to gamify our GRE prep process. Every day you input the number of hours you spend studying.Your points are calculated and stored for you to view.At the end of the week, you get a report of who is in lead. This person is also the winner for the week and will get a prize.For example, a prize could be a pack of Oreos, or maybe cup noodles or admin rights for the server. It can be decided on a weekly basis.\n\nUsage :-\n**$studied 5** # letting the bot know you studied for 5 hrs\n**$leaderboard** # show the leaderboard of the week\n**$prize shwarma**# Adding the prize of 'shwarma' to the pot\n**$show_prizes #show the prizes you might win at the end of the week**\n**$hlp** # show the usage\n"
  embed=discord.Embed(title="Sample Embed", description=hlp, color=0xFF5733)
  await ctx.send(embed=embed)

@bot.command()
async def show_prizes(ctx):
  prizes = db["prizes"].value
  if bool(prizes):
    s=''
    for i in prizes:
      s += i+"\n" 

    await ctx.send(s)
  else:
    await ctx.send("Oops! no prizes suggested yet! to suggest a prize use the command **$prize <the prize>**")

# menu = DefaultMenu(page_left="\U0001F44D", page_right="👎", remove=":discord:743511195197374563", active_time=5)
# ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"




@bot.command()
async def reset_db(ctx):
  db["score"] = {}
  db["prizes"] = []

bot.loop.create_task(announce_winners())
bot.loop.create_task(reset())
keep_alive()
bot.run(os.getenv('TOKEN'))