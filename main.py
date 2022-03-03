import base64
import requests
from keep_alive import keep_alive

import discord
from discord.ext import commands
from discord import guild
#from discord_slash import SlashCommand, SlashContext
#from discord_slash.utils.manage_commands import create_choice, create_option
from discord import DMChannel
import os
import requests
import json
import time
import re
from replit import db
import asyncio
import math
import html
import maya
from treelib import Node, Tree
from getinfo import getinfo
import random

#https://stackoverflow.com/questions/38491722/reading-a-github-file-using-python-returns-html-tags
'''
url = 'https://raw.githubusercontent.com/DesmoSearch/DesmoSearch/main/data/thetitles.json'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    req = req.json()
    print(len(req))
    db['thetitles']=req
else:
    print('Content was not found.')
'''

print(db.keys())
ParentGraphsList=db['ParentGraphsList']
thetitles=db['thetitles']
GraphsList=db['GraphsList']
objowner=db['objowner']
noofresults=5;
TheDates=db['TheDates']

'''Gtree = Tree()
Gtree.create_node("Graphs", "Graphs")
for iI2 in range(len(GraphsList)):
  Gtree.create_node(GraphsList[iI2],  GraphsList[iI2]   , parent='Graphs')
print('part 1')
for iI3 in range(len(GraphsList)):
  if Gtree.contains(ParentGraphsList[iI3]):
    Gtree.move_node(GraphsList[iI3], ParentGraphsList[iI3])
print('treedone')'''

client = commands.Bot(command_prefix="_")
#slash = SlashCommand(client, sync_commands=True)
token = os.environ.get("DISCORD_BOT_SECRET")

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f"on {len(client.guilds)} servers | {db['searches']} searches done!"))

@client.event
async def on_raw_reaction_add(payload):
  emoji=payload.emoji
  user=payload.member
  messageid=payload.message_id
  channelid=payload.channel_id
  channel0 = client.get_channel(channelid)
  message0 = await channel0.fetch_message(messageid)
  if user.id==client.user.id:
    return
  elif emoji.name=='✅' and user.id==686012491607572515 and channelid==945245411449372702:
    def combine(gifs0,users0):
      result = [None]*(len(gifs0)+len(users0))
      result[1::2]=gifs0
      result[0::2]=users0
      return(' , '.join(result))
    channel = client.get_channel(948482596197777442)
    gifs=[]
    users=[]
    async for msg in channel.history(limit=1):
      damsg=msg
      C=(msg.content.replace(" ", "")).split(",")
      gifs.extend(C[1::2])
      users.extend(C[0::2])
    ###
    pattern=re.compile(r"((http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png))")
    gifs2=([mm.url for mm in message0.attachments]+[ii.group(1) for ii in pattern.finditer(message0.content)])
    users2=[str(message0.author.id) for i in range(len(gifs2))]
    if len(combine(gifs+gifs2,users+users2))<2000 and damsg.author.id==944269890301345884:
      await damsg.edit(content=combine(gifs+gifs2,users+users2))
    else:
      await channel.send(content=combine(gifs2,users2))

  elif emoji.name=='🔭':
    #code from on_message under the (!desmos link) elif
    pattern02=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
    x02=pattern02.finditer(message0.content)
    if len(list(x02))>0:
      thehash01=[ii.group(1) for ii in pattern02.finditer(message0.content)][0]
      msg2 = await message0.reply(embed=await getready(message0),mention_author=False)
      first_run2 = True
      dachoose2=[1,0,0]
      while True:
        if first_run2:
            first_run2 = False
            dachoose2=[None,thehash01,[thehash01]]
            dachoose2=await aboutchain(message0,thehash01,msg2,[True,-10,'','',dachoose2])
  
        reactmoji2=[]
        
        reactmoji2.append('✅')
        if str(message0.author.id)=='686012491607572515':
           reactmoji2.append('❌')
  
  
        for react2 in reactmoji2:
            await msg2.add_reaction(react2)
            
  
        def check_react(reaction, user):
            if reaction.message.id != msg2.id:
                return False
            if user != message0.author:
                return False
            if str(reaction.emoji) not in reactmoji2 and str(reaction.emoji) not in ['👈','👉','🖱️']:
                return False
            return True
  
        try:
            res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
        except asyncio.TimeoutError:
            return await msg2.clear_reactions()
        if user2 != message0.author:
            pass
        elif '✅' in str(res2.emoji):
            return await msg2.clear_reactions()
        elif '❌' in str(res2.emoji):
            return await msg2.delete()
        elif '🖱️' in str(res2.emoji) or '👈' in str(res2.emoji) or '👉' in str(res2.emoji):
            dachoose2=await aboutchain(message0,thehash01,msg2,[True,-10,res2,user2,dachoose2])

      
    

@client.event
async def on_message(message): 
  pattern=re.compile(r"!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?")
  x=pattern.finditer(message.content)
  pattern02=re.compile(r"!https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
  x02=pattern02.finditer(message.content)
  pattern03=re.compile(r"(!graph ([^?]+)(?: *\?(?:(x|y|size)(?:=(\[.*?,.*?\]))?)(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?)?)")
  x03=pattern03.finditer(message.content)
  if message.author == client.user:
    return
  elif len(list(x))==1:
    msg = await message.channel.send(embed=await getready(message))
    async with message.channel.typing():
      searchterm=[ii.group(1) for ii in pattern.finditer(message.content)][0]
      parameterterm = [[ii.group(iii) for ii in pattern.finditer(message.content)][0] for iii in [2,4,6]]
      searchterm1=[ii.group(3) for ii in pattern.finditer(message.content)][0]
      searchterm2=[ii.group(5) for ii in pattern.finditer(message.content)][0]
      searchterm3=[ii.group(7) for ii in pattern.finditer(message.content)][0]
      if checkIfDuplicates(parameterterm):
        parameterterm=[None,None,None]
        searchterm1=""
        searchterm2=""
        searchterm3=""
  
      titlecond = True if parameterterm==[None,None,None] else ('title' in parameterterm)
      ownercond = True if parameterterm==[None,None,None] else ('owner' in parameterterm)
      hashcond = True if parameterterm==[None,None,None] else ('hash' in parameterterm)
      slashcheckterm,slashcheck1,slashcheck2,slashcheck3=False,False,False,False
      if "/" in searchterm:
        searchterm=searchterm[1:-1]
        slashcheckterm=True
      else:
        searchterm=searchterm.lower()
      if searchterm1 is None:
        searchterm1 = ""
      elif "/" in searchterm1:
        searchterm1=searchterm1[1:-1]
        slashcheck1=True
      else:
        searchterm1=searchterm1.lower()
      if searchterm2 is None:
        searchterm2 = ""
      elif "/" in searchterm2:
        searchterm2=searchterm2[1:-1]
        slashcheck2=True
      else:
        searchterm2=searchterm2.lower()
      if searchterm3 is None:
        searchterm3 = ""
      elif "/" in searchterm3:
        searchterm3=searchterm3[1:-1]
        slashcheck3=True
      else:
        searchterm3=searchterm3.lower()
      
      print(f'"{searchterm}"')
  
      searchterm0sub=[searchterm1,searchterm2,searchterm3]
      slashchecks=[slashcheck1,slashcheck2,slashcheck3]
      searchtermtitle, searchtermhash, searchtermowner = "", "", "" 
      slashtitlecheck, slashhashcheck, slashownercheck = False,False,False
      try:
        searchtermtitle=searchterm0sub[parameterterm.index('title')]
        slashtitlecheck=slashchecks[parameterterm.index('title')]
      except ValueError:
        searchtermtitle=""
      try:
        searchtermhash=searchterm0sub[parameterterm.index('hash')]
        slashhashcheck=slashchecks[parameterterm.index('hash')]
      except ValueError:
        searchtermhash=""
      try:
        searchtermowner=searchterm0sub[parameterterm.index('owner')]
        slashownercheck=slashchecks[parameterterm.index('owner')]
      except ValueError:
        searchtermowner=""
        
  
      searchtermpart = lambda data00 : data00 if slashcheckterm else data00.lower()
      searchterm0 = searchtermpart(searchterm)
      titlepart = lambda data00 : data00 if slashtitlecheck else data00.lower()
      hashpart = lambda data00 : data00 if slashhashcheck else data00.lower()
      ownerpart = lambda data00 : data00 if slashownercheck else data00.lower()
      
      searchresult = [hash for hash, title in thetitles.items() if (titlecond*bool(re.search(searchterm0, searchtermpart(str(title)))) or hashcond*bool(re.search(searchterm0, str(hash))) or ownercond*bool(re.search(searchterm0, searchtermpart(str(objowner.get(str(hash),None)))))) and (bool(re.search(titlepart(searchtermtitle), titlepart(str(title)))) and bool(re.search(hashpart(searchtermhash), hashpart(str(hash)))) and bool(re.search(ownerpart(searchtermowner), ownerpart(str(objowner.get(str(hash),None))))))]

    #https://gist.github.com/noaione/58cdd25a1cc19388021deb0a77582c97
    max_page=math.ceil(len(searchresult)/noofresults)
    first_run = True
    num = 1
    Gnum = 1
    GnumDisplay=0
    infograph=0
    dachoose=[1,0,0]
    while True:
      if first_run:
          first_run = False
          await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))

      reactmoji = []

      if max_page == 1 and num == 1:
          pass
      elif num == 1:
          reactmoji.append('⏩')
      elif num == max_page:
          reactmoji.append('⏪')
      elif num > 1 and num < max_page:
          reactmoji.extend(['⏪', '⏩'])

      if len(searchresult) == 1 and Gnum == 1 and GnumDisplay==1:
          pass
      elif Gnum == 1:
          reactmoji.append('🔽')
      elif Gnum == len(searchresult) :
          reactmoji.append('🔼')
      elif Gnum > 1 and Gnum<len(searchresult):
          reactmoji.extend(['🔼', '🔽'])

      reactmoji.append('✅')
      if str(message.author.id)=='686012491607572515':
         reactmoji.append('❌')
      if GnumDisplay==1:
        reactmoji.append('🔎')

      for react in reactmoji:
          await msg.add_reaction(react)
          

      def check_react(reaction, user):
          if reaction.message.id != msg.id:
              return False
          if user != message.author:
              return False
          if str(reaction.emoji) not in reactmoji and str(reaction.emoji) not in ['👈','👉','🖱️']:
              return False
          return True

      try:
          res, user = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
      except asyncio.TimeoutError:
          return await msg.clear_reactions()
      if user != message.author:
          pass
      elif '⏪' in str(res.emoji):
          num = num - 1
          Gnum = (num-1)*noofresults+1
          GnumDisplay=0
          infograph=0
          await msg.clear_reactions()
          await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))
      elif '⏩' in str(res.emoji):
          num = num + 1
          Gnum = (num-1)*noofresults+1
          GnumDisplay=0
          infograph=0
          await msg.clear_reactions()
          await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))
      elif '🔽' in str(res.emoji):
          Gnum  = Gnum if GnumDisplay==0 else Gnum+1
          GnumDisplay=1
          num = math.ceil(Gnum/noofresults)
          await msg.clear_reactions()
          await msg.edit(embed=createembed(Gnum,num,searchresult,max_page,message))
      elif '🔼' in str(res.emoji):
          Gnum  = Gnum if GnumDisplay==0 else Gnum-1
          GnumDisplay=1
          num = math.ceil(Gnum/noofresults)
          await msg.clear_reactions()
          await msg.edit(embed=createembed(Gnum,num,searchresult,max_page,message))
      elif '✅' in str(res.emoji):
          return await msg.clear_reactions()
      elif '❌' in str(res.emoji):
          await message.delete()
          return await msg.delete()
      elif '🔎' in str(res.emoji):
          infograph=1-infograph
          await msg.clear_reactions()
          dachoose=[None,searchresult[Gnum-1],[searchresult[Gnum-1]]]

      
      if infograph==1:
        dachoose=await aboutchain(message,searchresult[Gnum-1],msg,[True,Gnum,res,user,dachoose])
      else:
        await msg.edit(embed=createembed(-1 if GnumDisplay==0 else Gnum,num,searchresult,max_page,message))
          
  elif len(list(x02))==1:
    
    
    thehash01=[ii.group(1) for ii in pattern02.finditer(message.content)][0]
    await message.edit(suppress=True)
    msg2 = await message.channel.send(embed=await getready(message))


    first_run2 = True
    dachoose2=[1,0,0]
    while True:
      if first_run2:
          first_run2 = False
          dachoose2=[None,thehash01,[thehash01]]
          dachoose2=await aboutchain(message,thehash01,msg2,[True,None,'','',dachoose2])

      reactmoji2=[]
      
      reactmoji2.append('✅')
      if str(message.author.id)=='686012491607572515':
         reactmoji2.append('❌')


      for react2 in reactmoji2:
          await msg2.add_reaction(react2)
          

      def check_react(reaction, user):
          if reaction.message.id != msg2.id:
              return False
          if user != message.author:
              return False
          if str(reaction.emoji) not in reactmoji2 and str(reaction.emoji) not in ['👈','👉','🖱️']:
              return False
          return True

      try:
          res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
      except asyncio.TimeoutError:
          return await msg2.clear_reactions()
      if user2 != message.author:
          pass
      elif '✅' in str(res2.emoji):
          return await msg2.clear_reactions()
      elif '❌' in str(res2.emoji):
          await message.delete()
          return await msg2.delete()
      elif '🖱️' in str(res2.emoji) or '👈' in str(res2.emoji) or '👉' in str(res2.emoji):
          dachoose2=await aboutchain(message,thehash01,msg2,[True,None,res2,user2,dachoose2])


  elif message.content=="!dhelp":
    await getready(message)
    
    helpembed=discord.Embed(title="Commands",description="!dhelp, !desmos, ![+desmoslink]")
    helpembed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
    await message.channel.send(embed=helpembed,content='')
    
  elif len(list(x03))==1:
    msg3 = await message.channel.send(embed=await getready(message))
    
    wholeterm3=[ii.group(1) for ii in pattern03.finditer(message.content)][0]
    searchterm3=[ii.group(2) for ii in pattern03.finditer(message.content)][0]
    parameterterm3 = [[ii.group(iii) for ii in pattern03.finditer(message.content)][0] for iii in [3,5,7]]
    searchterm13=[ii.group(4) for ii in pattern03.finditer(message.content)][0]
    searchterm23=[ii.group(6) for ii in pattern03.finditer(message.content)][0]
    searchterm33=[ii.group(8) for ii in pattern03.finditer(message.content)][0]
    if checkIfDuplicates(parameterterm3):
      parameterterm3=[None,None,None]
      searchterm13=""
      searchterm23=""
      searchterm33=""
    searchterm3sub=[searchterm13,searchterm23,searchterm33]
    searchtermx, searchtermy, searchtermsize = "[-10,10]", "[-10,10]", "[500,500]" 
    try:
      searchtermx=searchterm3sub[parameterterm3.index('x')]
    except ValueError:
      searchtermx="[-10,10]"
    try:
      searchtermy=searchterm3sub[parameterterm3.index('y')]
    except ValueError:
      searchtermy="[-10,10]"
    try:
      searchtermsize=searchterm3sub[parameterterm3.index('size')]
    except ValueError:
      searchtermsize="[500,500]"
    if json.loads(searchtermx)[1]-json.loads(searchtermx)[0]<0:
      searchtermx="[-10,10]"
    if json.loads(searchtermy)[1]-json.loads(searchtermy)[0]<0:
      searchtermy="[-10,10]"
    if (json.loads(searchtermsize)[0]<50 or json.loads(searchtermsize)[1]<50) or not (1/2<=json.loads(searchtermsize)[0]/json.loads(searchtermsize)[1]<=2):
      searchtermsize="[500,500]"
    
    xtick=AutomateXYLabels(json.loads(searchtermx)[0],json.loads(searchtermx)[1])
    ytick=AutomateXYLabels(json.loads(searchtermy)[0],json.loads(searchtermy)[1])
    searchterm3=searchterm3.replace(" ", "")
    print([searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick])
    first_run3 = True
    strlist = lambda x, y: f"[{x},{y}]"
    while True:
        reactmoji3 = []
        if first_run3:
            reactmoji3.extend(['🔄','➡️','⬆️','⬅️','⬇️','🔬','🔭','✅'])
            first_run3 = False
            await msg3.edit(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
          
        thex0=json.loads(searchtermx)[0]
        thex1=json.loads(searchtermx)[1]
        they0=json.loads(searchtermy)[0]
        they1=json.loads(searchtermy)[1]
        scalex=(thex1-thex0)/10
        scaley=(they1-they0)/10
        zoomf=1.5
        
        reactmoji3.extend(['🔄','➡️','⬆️','⬅️','⬇️','🔬','🔭','✅'])
        #['🔄','➡️','↗️','⬆️','↖️','⬅️','↙️','⬇️','↘️','➕','➖','✅']
        if str(message.author.id)=='686012491607572515':
           reactmoji3.append('❌')
  
        for react in reactmoji3:
            await msg3.add_reaction(react)

        def check_react(reaction, user):
            if reaction.message.id != msg3.id:
                return False
            if user != message.author:
                return False
            if str(reaction.emoji) not in reactmoji3:
                return False
            return True

        try:
            res3, user3 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
        except asyncio.TimeoutError:
            return await msg3.clear_reactions()
        if user3 != message.author:
            pass
        elif '✅' in str(res3.emoji):
            return await msg3.clear_reactions()
        elif '❌' in str(res3.emoji):
            await message.delete()
            return await msg3.delete()
        else:

          if '🔄' in str(res3.emoji):
              searchterm3=','.join(searchterm3.split(',')[1:]+searchterm3.split(',')[:1])

          if '➡️' in str(res3.emoji):
              thex0,thex1=thex0+scalex,thex1+scalex
              searchtermx=strlist(thex0,thex1)
              
              
          if '⬆️' in str(res3.emoji):
              they0,they1=they0+scaley,they1+scaley
              searchtermy=strlist(they0,they1)

              
          if '⬅️' in str(res3.emoji):
              thex0,thex1=thex0-scalex,thex1-scalex
              searchtermx=strlist(thex0,thex1)

              
          if '⬇️' in str(res3.emoji):
              they0,they1=they0-scaley,they1-scaley
              searchtermy=strlist(they0,they1)
              await message.remove_reaction('⬇️',message.author)

              
          if '🔬' in str(res3.emoji):
              thex0,thex1=(thex0+thex1)/2-(1/zoomf)*(thex1-thex0)/2,(thex0+thex1)/2+(1/zoomf)*(thex1-thex0)/2
              they0,they1=(they0+they1)/2-(1/zoomf)*(they1-they0)/2,(they0+they1)/2+(1/zoomf)*(they1-they0)/2
              thex0,thex1,they0,they1=round(thex0,2),round(thex1,2),round(they0,2),round(they1,2)
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              
          if '🔭' in str(res3.emoji):
              thex0,thex1=(thex0+thex1)/2-(zoomf)*(thex1-thex0)/2,(thex0+thex1)/2+(zoomf)*(thex1-thex0)/2
              they0,they1=(they0+they1)/2-(zoomf)*(they1-they0)/2,(they0+they1)/2+(zoomf)*(they1-they0)/2
              thex0,thex1,they0,they1=round(thex0,2),round(thex1,2),round(they0,2),round(they1,2)
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              

        xtick=AutomateXYLabels(json.loads(searchtermx)[0],json.loads(searchtermx)[1])
        ytick=AutomateXYLabels(json.loads(searchtermy)[0],json.loads(searchtermy)[1])
        print(res3.emoji)
        await msg3.remove_reaction(emoji= res3.emoji, member = user3) 
        print(searchtermx)
        print(searchtermy)
        await msg3.edit(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
  elif message.content=="!loading":
    await message.channel.send(embed=await getready(message))
          
    

    
#----------------------------------------------------------
async def getready(message):
  db['searches']=db['searches']+1
  await on_ready()
  await dmsend(repr(message)+"\n\n"+message.content)
  return await loadinggif(message)

async def dmsend(msg):
    user = await client.fetch_user("686012491607572515")
    await DMChannel.send(user,"```"+msg+"```")

async def loadinggif(msg0):
  channel = client.get_channel(948482596197777442)
  gifs=[]
  users=[]
  async for msg in channel.history(limit=10000):
    C=(msg.content.replace(" ", "")).split(",")
    gifs.extend(C[1::2])
    users.extend(C[0::2])
  selectR=random.randint(0,len(gifs)-1)
  user = await client.fetch_user(str(users[selectR]))
  embed=discord.Embed(title='Loading...') 
  embed.set_author(name='Gif by '+str(user), icon_url=user.avatar_url)
  embed.set_image(url=gifs[selectR])
  embed.set_footer(text='Shared in #looping-gifs in the https://dsc.gg/me314 discord server')
  return embed
    
##########
def graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick):
  thelink=f"https://graphsketch.com/render.php?eqn1_eqn={searchterm3}&x_min={json.loads(searchtermx)[0]}&x_max={json.loads(searchtermx)[1]}&y_min={json.loads(searchtermy)[0]}&y_max={json.loads(searchtermy)[1]}&image_w={json.loads(searchtermsize)[0]}&image_h={json.loads(searchtermsize)[1]}&do_grid=1&x_tick={xtick}&y_tick={ytick}&x_label_freq=5&y_label_freq=5"
  gembed=discord.Embed(title=wholeterm3,description=f"[Open image in a new tab]({thelink})")
  gembed.add_field(name="Graph(s)", value=searchterm3, inline=False)
  gembed.add_field(name="Domain", value=searchtermx, inline=True)
  gembed.add_field(name="Range", value=searchtermy, inline=True)
  gembed.add_field(name="Image Dimensions", value=f"[width,height]: {searchtermsize}", inline=False)
  gembed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
  gembed.set_image(url=thelink)
  return gembed

#######
async def aboutchain(message,thehash01,msg2,fromSearch):
  async with message.channel.typing():
    newhash=fromSearch[4][1] if fromSearch[0] else thehash01
    historylist=fromSearch[4][2] if fromSearch[0] else [thehash01]
    theinfo = getinfo("https://www.desmos.com/calculator/"+newhash)
    subgraphs = []
    if theinfo['parent_hash'] is not None:
      subgraphs.append(theinfo['parent_hash'])
    choose = fromSearch[4][0] if fromSearch[4][0] is not None else len(subgraphs)
    subgraphs.append(newhash)
    thevalue=','.join([GraphsList[i] for i in range(len(GraphsList)) if (newhash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
    if thevalue!="":
      subgraphs.extend(thevalue.split(','))

  reactmoji2 = []


  def check_react(reaction, user):
      if reaction.message.id != msg2.id:
          return False
      if user != message.author:
          return False
      if str(reaction.emoji) not in reactmoji2:
          return False
      return True
  res2, user2 = '',''
  try:
      if fromSearch[0]:
        res2, user2 = fromSearch[2], fromSearch[3]
      else:
        res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
  except asyncio.TimeoutError:
      return await msg2.clear_reactions()
  if user2 != message.author:
      pass
  elif '👉' in str(res2.emoji):
      choose=choose+1
  elif '👈' in str(res2.emoji):
      choose=choose-1
  elif '🖱️' in str(res2.emoji):
    newhash=subgraphs[choose%len(subgraphs)]
    choose=1
    historylist.append(newhash)
    subgraphs=[newhash]

  if res2!='' and user2!='':
    await msg2.remove_reaction(emoji= "👉", member = user2)
    await msg2.remove_reaction(emoji= "👈", member = user2)
    await msg2.remove_reaction(emoji= "🖱️", member = user2)
  await msg2.edit(embed=aboutembed(message,newhash,fromSearch,subgraphs[choose%len(subgraphs)],historylist),content='')
  reactmoji2.extend(['👈','👉','🖱️'])

  for react in reactmoji2:
      await msg2.add_reaction(react)

  return ([choose,newhash,historylist])

def aboutembed(message,thehash,fromSearch,underline,historylist):
  dainfo=getinfo("https://www.desmos.com/calculator/"+thehash)
  embed = discord.Embed(color=0x12793e, title=dainfo['title'],description="https://www.desmos.com/calculator/"+thehash)
  if 'thumbUrl' in dainfo.keys():
    embed.set_image(url=dainfo['thumbUrl'])
  if objowner.get(str(thehash),None) is not None:
    embed.add_field(name="Possible Author", value=objowner.get(str(thehash),None), inline=False)
  
  embed.add_field(name="Date Created", value="<t:"+str(round(maya.parse(dainfo['created']).datetime().timestamp()))+":F>", inline=True)
  embed.add_field(name="Version", value="```"+str(dainfo['version'])+"```", inline=True)
  if len([] if dainfo['notes'] is None else dainfo['notes'])>0 and len(str(dainfo['notes']))<=1020:
    embed.add_field(name="Notes", value="".join(f"\n{iii+1}. [#{str(dainfo['notes'][iii]['id'])}]{(dainfo['notes'][iii]['text'])}" for iii in range(len(dainfo['notes']))), inline=False)
  elif len(str(dainfo['notes']))>1020:
    embed.add_field(name="Notes", value="Contains "+str(len(dainfo['notes']))+" notes", inline=False)
  if len([] if dainfo['folders'] is None else dainfo['folders'])>0:
    embed.add_field(name="Folders", value="".join(f"\n{iii+1}. [#{str(dainfo['folders'][iii]['id'])}]{dainfo['folders'][iii]['title']}" for iii in range(len(dainfo['folders']))), inline=False)
  if len([] if dainfo['variables'] is None else dainfo['variables'])>0 and len(str(dainfo['variables']))<=1020:
    embed.add_field(name="Variables", value="```"+' , '.join(dainfo['variables'])+"```", inline=False)
  elif len(str(dainfo['variables']))>1020:
    embed.add_field(name="Variables", value="```"+"Contains "+str(len(dainfo['variables']))+" variables"+"```", inline=False)
  embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)

#history
  graphnodes=[]
  parentnodes=[]
  for newhash in historylist:
    theinfo0 = getinfo("https://www.desmos.com/calculator/"+newhash)
    if theinfo0['parent_hash'] is not None:
      graphnodes.append(theinfo0['parent_hash'])
    graphnodes.append(newhash)
    thevalue0=','.join([GraphsList[i] for i in range(len(GraphsList)) if (newhash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
    if thevalue0!="":
      graphnodes.extend(thevalue0.split(','))
  graphnodes=list(set(graphnodes))
  for iI in range(len(graphnodes)):
    Get=getinfo("https://www.desmos.com/calculator/"+graphnodes[iI])
    parentnodes.append(Get['parent_hash'])
  gtree = Tree()
  gtree.create_node("Graphs", "Graphs")
  for iI2 in range(len(graphnodes)):
    gtree.create_node(graphnodes[iI2],  graphnodes[iI2]   , parent='Graphs')
  for iI3 in range(len(graphnodes)):
    if gtree.contains(parentnodes[iI3]):
      gtree.move_node(graphnodes[iI3], parentnodes[iI3])
  gtree=str(gtree.show(line_type="ascii-ex",stdout=False))
  gtree='```ini\n'+(gtree).replace(underline,"["+underline+"]")+'```'

    
  if fromSearch[0] and fromSearch[1] is not None:
    if fromSearch[1]==-10:
      pattern020=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
      thehash010=[ii.group(1) for ii in pattern020.finditer(message.content)][0]
      embed.set_footer(text='First desmos url in the message: https://www.desmos.com/calculator/'+thehash010+'\n'+'→'.join(historylist))
    else:
      pattern2=re.compile(r"(!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
      searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
      ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
      embed.set_footer(text=ordinal(fromSearch[1])+" graph from \""+searchterm+"\"\n"+'→'.join(historylist))
  elif fromSearch[0] and fromSearch[1] is None:
    pattern020=re.compile(r"!https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
    thehash010=[ii.group(1) for ii in pattern020.finditer(message.content)][0]
    embed.set_footer(text='!https://www.desmos.com/calculator/'+thehash010+'\n'+'→'.join(historylist))
  
  if dainfo['parent_hash'] is not None:
    embed.add_field(name="Parent Graph", value=("__**"+dainfo['parent_hash']+"**__" if dainfo['parent_hash']==underline else dainfo['parent_hash']), inline=True)
  embed.add_field(name="Current Graph", value=("__**"+thehash+"**__" if thehash==underline else thehash), inline=True)
  davalue=' , '.join([("__**"+GraphsList[i]+"**__" if GraphsList[i]==underline else GraphsList[i]) for i in range(len(GraphsList)) if (thehash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
  if davalue!="":
    embed.add_field(name="Child Graphs", value=davalue, inline=True)
  embed.add_field(name="Des[sub]Tree", value=gtree, inline=False)
  
  return embed



############
def createembed(Gnum,num,result,max_page,message):
  datahashes=result[noofresults*(num-1):noofresults*num+1]
  thedescription="".join(f'{"> __**" if Gnum==(num-1)*noofresults+i+1 else ""}{(num-1)*noofresults+i+1}. {"" if objowner.get(str(datahashes[i]),None) is None else str(objowner.get(str(datahashes[i]),None))+": "}[{thetitles[datahashes[i]]}](https://www.desmos.com/calculator/{datahashes[i]}){"**__" if Gnum==(num-1)*noofresults+i+1 else ""}\n'for i in range(len(datahashes)))
  
  pattern2=re.compile(r"!desmos (([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
  searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
  embed = discord.Embed(color=0x12793e, title=str(len(result))+" graphs for \""+searchterm+"\"",description=thedescription)
  embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
  embed.set_footer(text="Page: "+str(num)+"/"+str(max_page))
  if Gnum>-1:
    dahash=result[Gnum-1]
    #dainfo=getinfo("https://www.desmos.com/calculator/"+dahash)
    embed.set_image(url=f"https://saved-work.desmos.com/calc_thumbs/production/{dahash}.png")
    embed.add_field(name="Graph Selected:", value=f"https://www.desmos.com/calculator/{dahash}", inline=False)
    
    #embed.add_field(name="Date Created", value=dainfo['date'], inline=False)
  return embed

def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    listOfElems=list(filter((None).__ne__, listOfElems))
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

#https://studio.code.org/projects/applab/kEUCxMdKd7P-a1y4zo4cO3IQasxWXeHipAoDwk1dS4w/view
def AutomateXYLabels(first,second):
  XLabel=(second-first)/5
  NumberOfDigits=round(math.log(XLabel,10))
  NearestArray=[1,2,5]
  MultiplyNearestArrayBy = [NumberOfDigits-1,NumberOfDigits]
  XLabelList = [NearestArray[j]*(10**MultiplyNearestArrayBy[i]) for i in range(2) for j in range(3)];
  LeastDiff = [abs(NearestArray[j]*(10**MultiplyNearestArrayBy[i])-XLabel) for i in range(2) for j in range(3)];
  XLabel=XLabelList[LeastDiff.index(min(LeastDiff))]
  return (XLabel/5)


keep_alive()
client.run(token)