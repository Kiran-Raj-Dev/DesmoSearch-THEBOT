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
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html

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

client = commands.Bot(command_prefix="_")
#slash = SlashCommand(client, sync_commands=True)
token = os.environ.get("DISCORD_BOT_SECRET")

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f"on {len(client.guilds)} servers | {db['searches']} searches done!"))

@client.event
async def on_message(message): 
  pattern=re.compile(r"!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?")
  x=pattern.finditer(message.content)
  pattern02=re.compile(r"!https:\/\/www.desmos.com\/calculator\/([a-z0-9]{10})")
  x02=pattern02.finditer(message.content)
  pattern03=re.compile(r"(!graph ([^?]+)(?: *\?(?:(x|y|size)(?:=(\[.*?,.*?\]))?)(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?)?)")
  x03=pattern03.finditer(message.content)
  if message.author == client.user:
    return
  elif len(list(x))==1:
    await getready(message)
    
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
    
    if "/" in searchterm:
      searchterm=searchterm[1:-1]
    else:
      searchterm=searchterm.lower()
    if searchterm1 is None:
      searchterm1 = ""
    elif "/" in searchterm1:
      searchterm1=searchterm1[1:-1]
    else:
      searchterm1=searchterm1.lower()
    if searchterm2 is None:
      searchterm2 = ""
    elif "/" in searchterm2:
      searchterm2=searchterm2[1:-1]
    else:
      searchterm2=searchterm2.lower()
    if searchterm3 is None:
      searchterm3 = ""
    elif "/" in searchterm3:
      searchterm3=searchterm3[1:-1]
    else:
      searchterm3=searchterm3.lower()
    
    print(f'"{searchterm}"')

    searchterm0sub=[searchterm1,searchterm2,searchterm3]
    searchtermtitle, searchtermhash, searchtermowner = "", "", "" 
    try:
      searchtermtitle=searchterm0sub[parameterterm.index('title')]
    except ValueError:
      searchtermtitle=""
    try:
      searchtermhash=searchterm0sub[parameterterm.index('hash')]
    except ValueError:
      searchtermhash=""
    try:
      searchtermowner=searchterm0sub[parameterterm.index('owner')]
    except ValueError:
      searchtermowner=""
    
    searchresult = [hash for hash, title in thetitles.items() if (titlecond*bool(re.search(searchterm, str(title))) or hashcond*bool(re.search(searchterm, str(hash))) or ownercond*bool(re.search(searchterm, str(objowner.get(str(hash),None))))) and (bool(re.search(searchtermtitle, str(title))) and bool(re.search(searchtermhash, str(hash))) and bool(re.search(searchtermowner, str(objowner.get(str(hash),None)))))]

    #https://gist.github.com/noaione/58cdd25a1cc19388021deb0a77582c97
    max_page=math.ceil(len(searchresult)/noofresults)
    first_run = True
    num = 1
    Gnum = 1
    GnumDisplay=0
    infograph=0
    while True:
        if first_run:
            first_run = False
            msg = await message.channel.send(embed=createembed(-1,num,searchresult,max_page,message))

        reactmoji = []

        if max_page == 1 and num == 1:
            pass
        elif num == 1:
            reactmoji.append('⏩')
        elif num == max_page:
            reactmoji.append('⏪')
        elif num > 1 and num < max_page:
            reactmoji.extend(['⏪', '⏩'])

        if len(searchresult) == 1 and Gnum == 0:
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
            if str(reaction.emoji) not in reactmoji:
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
        if infograph==1:
          await aboutchain(message,searchresult[Gnum-1],msg,[True,Gnum])
        else:
          await msg.edit(embed=createembed(-1 if GnumDisplay==0 else Gnum,num,searchresult,max_page,message))
          
  elif len(list(x02))==1:
    
    db['searches']=db['searches']+1
    await on_ready()
    await dmsend(repr(message)+"\n\n"+message.content)
    
    thehash01=[ii.group(1) for ii in pattern02.finditer(message.content)][0]
    await message.edit(suppress=True)
    msg2 = await message.channel.send("🔎")
    await aboutchain(message,thehash01,msg2,[False])

  elif message.content=="!dhelp":
    await getready(message)
    
    helpembed=discord.Embed(title="Commands",description="!dhelp, !desmos, ![+desmoslink]")
    helpembed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
    await message.channel.send(embed=helpembed,content='')
  elif len(list(x03))==1:
    await getready(message)
    
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
        if first_run3:
            first_run3 = False
            msg3 = await message.channel.send(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
          
        thex0=json.loads(searchtermx)[0]
        thex1=json.loads(searchtermx)[1]
        they0=json.loads(searchtermy)[0]
        they1=json.loads(searchtermy)[1]
        scalex=(thex1-thex0)/10
        scaley=(they1-they0)/10
        zoomf=1.5
        reactmoji3 = []
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
              
          if '↗️' in str(res3.emoji):
              thex0,thex1=thex0+scalex,thex1+scalex
              they0,they1=they0+scaley,they1+scaley
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              
          if '⬆️' in str(res3.emoji):
              they0,they1=they0+scaley,they1+scaley
              searchtermy=strlist(they0,they1)
              
          if '↖️' in str(res3.emoji):
              thex0,thex1=thex0-scalex,thex1-scalex
              they0,they1=they0+scaley,they1+scaley
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              
          if '⬅️' in str(res3.emoji):
              thex0,thex1=thex0-scalex,thex1-scalex
              searchtermx=strlist(thex0,thex1)
              
          if '↙️' in str(res3.emoji):
              thex0,thex1=thex0-scalex,thex1-scalex
              they0,they1=they0-scaley,they1-scaley
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              
          if '⬇️' in str(res3.emoji):
              they0,they1=they0-scaley,they1-scaley
              searchtermy=strlist(they0,they1)
              await message.remove_reaction('⬇️',message.author)
              
          if '↘️' in str(res3.emoji):
              thex0,thex1=thex0+scalex,thex1+scalex
              they0,they1=they0-scaley,they1-scaley
              searchtermx=strlist(thex0,thex1)
              searchtermy=strlist(they0,they1)
              
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
        for ddemo in ['🔄','➡️','⬆️','⬅️','⬇️','🔬','🔭','✅']:
          await message.remove_reaction(ddemo, message.author)
        await msg3.edit(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
          
    

    
#----------------------------------------------------------
def graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick):
  thelink=f"https://graphsketch.com/render.php?eqn1_eqn={searchterm3}&x_min={json.loads(searchtermx)[0]}&x_max={json.loads(searchtermx)[1]}&y_min={json.loads(searchtermy)[0]}&y_max={json.loads(searchtermx)[1]}&image_w={json.loads(searchtermsize)[0]}&image_h={json.loads(searchtermsize)[1]}&do_grid=1&x_tick={xtick}&y_tick={ytick}&x_label_freq=5&y_label_freq=5"
  gembed=discord.Embed(title=wholeterm3,description=f"[Open image in a new tab]({thelink})")
  gembed.add_field(name="Graph(s)", value=searchterm3, inline=False)
  gembed.add_field(name="Domain", value=searchtermx, inline=True)
  gembed.add_field(name="Range", value=searchtermy, inline=True)
  gembed.add_field(name="Image Dimensions", value=f"[width,height]: {searchtermsize}", inline=False)
  gembed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
  gembed.set_image(url=thelink)
  return gembed

  
async def getready(message):
  db['searches']=db['searches']+1
  await on_ready()
  await dmsend(repr(message)+"\n\n"+message.content)
  
async def aboutchain(message,thehash01,msg2,fromSearch):
  theembed=aboutembed(thehash01,message)
  dainfo0=getinfo("https://www.desmos.com/calculator/"+thehash01)
  if fromSearch[0]:
    pattern2=re.compile(r"(!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
    searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
    ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
    theembed.set_footer(text=ordinal(fromSearch[1])+" graph from \""+searchterm+"\"")
  else:
    theembed.set_footer(text='!https://www.desmos.com/calculator/'+thehash01)
  
  if dainfo0['parent_hash'] is not None:
    theembed.add_field(name="Parent Graph", value=dainfo0['parent_hash'], inline=True)
  davalue=' , '.join([GraphsList[i] for i in range(len(GraphsList)) if (thehash01 in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
  if davalue!="":
    theembed.add_field(name="Child Graphs", value=davalue, inline=True)
  
  await msg2.edit(embed=theembed,content='')

def aboutembed(thehash,message):
  dainfo=getinfo("https://www.desmos.com/calculator/"+thehash)
  embed = discord.Embed(color=0x19212d, title=dainfo['title'],description="https://www.desmos.com/calculator/"+thehash)
  embed.set_image(url=dainfo['thumbUrl'])
  if objowner.get(str(thehash),None) is not None:
    embed.add_field(name="Possible Author", value=objowner.get(str(thehash),None), inline=False)
  embed.add_field(name="Date Created", value="```"+dainfo['created']+"```", inline=True)
  embed.add_field(name="Version", value="```"+str(dainfo['version'])+"```", inline=True)
  if len([] if dainfo['notes'] is None else dainfo['notes'])>0 and len(str(dainfo['notes']))<=1020:
    embed.add_field(name="Notes", value="".join(f"\n{iii+1}. [#{str(dainfo['notes'][iii]['id'])}]{(dainfo['notes'][iii]['text'])}" for iii in range(len(dainfo['notes']))), inline=False)
  elif len(str(dainfo['notes']))>1020:
    print('hhhi')
    embed.add_field(name="Notes", value="Contains "+str(len(dainfo['notes']))+" notes", inline=False)
  if len([] if dainfo['folders'] is None else dainfo['folders'])>0:
    embed.add_field(name="Folders", value="".join(f"\n{iii+1}. [#{str(dainfo['folders'][iii]['id'])}]{dainfo['folders'][iii]['title']}" for iii in range(len(dainfo['folders']))), inline=False)
  if len([] if dainfo['variables'] is None else dainfo['variables'])>0 and len(str(dainfo['variables']))<=1020:
    embed.add_field(name="Variables", value="```"+' , '.join(dainfo['variables'])+"```", inline=False)
  elif len(str(dainfo['variables']))>1020:
    embed.add_field(name="Variables", value="```"+"Contains "+str(len(dainfo['variables']))+" variables"+"```", inline=False)
  embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
  
  return embed

def getinfo(hashurl):
  html = urlopen(hashurl).read()
  soup = BeautifulSoup(html, features="html.parser")
  finaldict={}
  
  for key in ['hash','parent_hash','thumbUrl','stateUrl','title','access','created']:
    finaldict[key]=json.loads(soup.body['data-load-data'])['graph'][key]
  finaldict['version']=json.loads(soup.body['data-load-data'])['graph']['state']['version']
  expr=(json.loads(soup.body['data-load-data'])['graph']['state'])['expressions']['list']
  finaldict['expressions'] = expr
  finaldict['notes']=[expr[i] for i in range(len(expr)) if expr[i]['type']=='text']
  finaldict['folders']=[expr[i] for i in range(len(expr)) if expr[i]['type']=='folder']
  patternvar = re.compile(r"([A-Za-z](?:_{?\w*}?)?)=")
  finaldict['variables']=list(set([ii.group(1) for ii in patternvar.finditer(str(expr))]))
  return (finaldict)

############
def createembed(Gnum,num,result,max_page,message):
  datahashes=result[noofresults*(num-1):noofresults*num+1]
  thedescription="".join(f'{"> __**" if Gnum==(num-1)*noofresults+i+1 else ""}{(num-1)*noofresults+i+1}. {"" if objowner.get(str(datahashes[i]),None) is None else str(objowner.get(str(datahashes[i]),None))+": "}[{thetitles[datahashes[i]]}](https://www.desmos.com/calculator/{datahashes[i]}){"**__" if Gnum==(num-1)*noofresults+i+1 else ""}\n'for i in range(len(datahashes)))
  
  pattern2=re.compile(r"!desmos (([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
  searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
  embed = discord.Embed(color=0x19212d, title=str(len(result))+" graphs for \""+searchterm+"\"",description=thedescription)
  embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
  embed.set_footer(text="Page: "+str(num)+"/"+str(max_page))
  if Gnum>-1:
    dahash=result[Gnum-1]
    #dainfo=getinfo("https://www.desmos.com/calculator/"+dahash)
    embed.set_image(url=f"https://saved-work.desmos.com/calc_thumbs/production/{dahash}.png")
    embed.add_field(name="Graph Selected:", value=f"https://www.desmos.com/calculator/{dahash}", inline=False)
    
    #embed.add_field(name="Date Created", value=dainfo['date'], inline=False)
  return embed
  
async def dmsend(msg):
    user = await client.fetch_user("686012491607572515")
    await DMChannel.send(user,"```"+msg+"```")


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

def getinfo0(url):
  fp = urllib.request.urlopen(url)
  mybytes = fp.read()
  
  mystr = mybytes.decode("utf8")
  fp.close()
  patternparent = re.compile(r"quot;parent_hash&quot;:&quot;([a-z0-9]{10,20})&quot;")
  parentGraph=None if len(list(patternparent.finditer(mystr)))==0 else [ii.group(1) for ii in patternparent.finditer(mystr)][0]
  patterndate = re.compile(r"created&quot;:&quot;(.*?)&quot")
  dateofGraph=[ii.group(1) for ii in patterndate.finditer(mystr)][0]
  patternnote = re.compile(r"&quot;text&quot;:&quot;(.*?)&quot")
  notes=None if len(list(patternnote.finditer(mystr)))==0 else [ii.group(1) for ii in patternnote.finditer(mystr)]
  patternfolder = re.compile(r"&quot;type&quot;:&quot;folder&quot;,&quot;id&quot;:&quot;[0-9]*&quot;,&quot;title&quot;:&quot;(.*?)&quot;")
  folders=None if len(list(patternfolder.finditer(mystr)))==0 else [ii.group(1) for ii in patternfolder.finditer(mystr)]
  patternvar = re.compile(r";(.(?:_{?\w*}?)?)=")
  variables=None if len(list(patternvar.finditer(mystr)))==0 else [ii.group(1) for ii in patternvar.finditer(mystr)]
  return {"parentGraph":parentGraph,"date":dateofGraph,"folders":folders,"notes":notes,"variables":list(set(variables)),"entire":mystr}

keep_alive()
client.run(token)