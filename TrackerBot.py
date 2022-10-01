import discord
import time
from discord.ext import commands, tasks
from datetime import datetime
from discord.utils import get

bot = commands.Bot(command_prefix = '/', case_insensitive = True)
bot.remove_command('help')

otrades = []
todtrades = []
wtrades = []

cmdChannelId = 776284217629737011

serverList= [[764264878755020850, 765777392777691188, 784629373571301397], [780143086751711322, 808534558819090482, 0]]

async def embedSend(embed):
    for i in range(len(serverList)):
        currentServer = serverList[i]
        guild = bot.get_guild(currentServer[0])
        channel = bot.get_channel(currentServer[1])
        if(currentServer[2]!=0):
            role = get(guild.roles, id=currentServer[2])
            send = await channel.send(f"{role.mention} @everyone",embed = embed)
        else:
            send = await channel.send("@everyone",embed = embed)
        if(currentServer[1]==765777392777691188):
            await send.add_reaction("<a:acegif:796407661830340688>")
        elif(currentServer[1]==808534558819090482):
            await send.add_reaction("✅")

@bot.event
async def on_ready():
    print('bot is ready')

@bot.command()
async def info(ctx):
    if(ctx.channel.id == cmdChannelId):
        await ctx.send("Open Trades List: "+str(otrades))
        await ctx.send("Today's Trades List: "+str(todtrades))
        if(len(wtrades)>25):
            await ctx.send("This Week's Trades List: "+str(wtrades[:24]))
            await ctx.send(str(wtrades[25:]))
        else:
            await ctx.send("This Week's Trades List: "+str(wtrades))

@bot.command(pass_context = True , aliases=['buy'])
async def BTO(ctx, ticker, strike, exp, pprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        ticker = ticker.upper()
        strike = strike.upper()
        if(comment!=None):
            embed = discord.Embed(
                colour = discord.Colour.dark_green(),
                title = "BTO "+ticker+" "+strike+" "+exp+" at "+pprice,
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.dark_green(),
                title = "BTO "+ticker+" "+strike+" "+exp+" at "+pprice,
                timestamp = datetime.utcnow()
            )
        valList = [ticker, strike, exp, pprice]
        try:
            otrades[otrades.index(0)] = valList
        except ValueError:
            otrades.append(valList)
        embed.set_footer(text = "ID: "+str(otrades.index(valList)+1))
        await embedSend(embed)

@bot.command(pass_context = True , aliases=['sell'])
async def STC(ctx, id, sprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        pprice = valList[3]
        perchange = round((((float(sprice)/float(pprice))-1)*100), 2)
        if(perchange>0):
            perchange = "+"+str(perchange)
        else:
            perchange = str(perchange)
        if(comment!=None):
            embed = discord.Embed(
                colour = discord.Colour.red(),
                title = "STC "+valList[0]+" "+valList[1]+" "+valList[2]+" at "+sprice+" from "+pprice+" ("+perchange+"%)",
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.red(),
                title = "STC "+valList[0]+" "+valList[1]+" "+valList[2]+" at "+sprice+" from "+pprice+" ("+perchange+"%)",
                timestamp = datetime.utcnow()
            )
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)
        valList = [valList[0], valList[1], valList[2], pprice, sprice, perchange]
        todtrades.append(valList)
        wtrades.append(valList)
        otrades[int(id)-1] = 0
        if(otrades.count(0) == len(otrades)):
            otrades.clear()

@bot.command()
async def LoadBTO(ctx, ticker, strike, exp, pprice):
    if(ctx.channel.id == cmdChannelId):
        ticker = ticker.upper()
        strike = strike.upper()
        valList = [ticker, strike, exp, pprice]
        try:
            otrades[otrades.index(0)] = valList
            await ctx.send("Added!")
        except ValueError:
            otrades.append(valList)
            await ctx.send("Added!")

@bot.command()
async def LoadSTC(ctx, id, sprice):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        pprice = valList[3]
        perchange = round((((float(sprice)/float(pprice))-1)*100), 2)
        if(perchange>0):
            perchange = "+"+str(perchange)
        else:
            perchange = str(perchange)
        valList = [valList[0], valList[1], valList[2], pprice, sprice, perchange]
        todtrades.append(valList)
        wtrades.append(valList)
        otrades[int(id)-1] = 0
        if(otrades.count(0) == len(otrades)):
            otrades.clear()
        await ctx.send("Sold!")

@bot.command()
async def BS(ctx, ticker, pprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        ticker = ticker.upper()
        if(comment!=None):
            embed = discord.Embed(
                colour = discord.Colour.dark_green(),
                title = "BTO "+ticker+" shares at "+pprice,
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.dark_green(),
                title = "BTO "+ticker+" shares at "+pprice,
                timestamp = datetime.utcnow()
            )
        valList = [ticker, pprice]
        try:
            otrades[otrades.index(0)] = valList
        except ValueError:
            otrades.append(valList)
        embed.set_footer(text = "ID: "+str(otrades.index(valList)+1))
        await embedSend(embed)

@bot.command()
async def SS(ctx, id, sprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        pprice = valList[1]
        perchange = round((((float(sprice)/float(pprice))-1)*100), 2)
        if(perchange>0):
            perchange = "+"+str(perchange)
        else:
            perchange = str(perchange)
        if(comment!=None):
            embed = discord.Embed(
                colour = discord.Colour.red(),
                title = "STC "+valList[0]+" shares at "+sprice+" from "+pprice+" ("+perchange+"%)",
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.red(),
                title = "STC "+valList[0]+" shares at "+sprice+" from "+pprice+" ("+perchange+"%)",
                timestamp = datetime.utcnow()
            )
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)
        valList = [valList[0], pprice, sprice, perchange]
        todtrades.append(valList)
        wtrades.append(valList)
        otrades[int(id)-1] = 0
        if(otrades.count(0) == len(otrades)):
            otrades.clear()

@bot.command()
async def cut(ctx, id, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        if(len(valList)==2):
            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = "CUT "+valList[0]+" shares (Stopped out)",
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = "CUT "+valList[0]+" shares (Stopped out)",
                    timestamp = datetime.utcnow()
                )
            valList = [valList[0]]
        else:
            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = "CUT "+valList[0]+" "+valList[1]+" "+valList[2]+" (Stopped out)",
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = "CUT "+valList[0]+" "+valList[1]+" "+valList[2]+" (Stopped out)",
                    timestamp = datetime.utcnow()
                )
            valList = [valList[0], valList[1], valList[2]]
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)
        todtrades.append(valList)
        wtrades.append(valList)
        otrades[int(id)-1] = 0
        if(otrades.count(0) == len(otrades)):
            otrades.clear()

@bot.command()
async def update(ctx, id, *, comment):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        if(len(valList)==2):
            embed = discord.Embed(
                colour = discord.Colour.purple(),
                title = "Update: "+valList[0]+" shares at "+valList[1],
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.purple(),
                title = "Update: "+valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[3],
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)

@bot.command()
async def trim(ctx, id, tprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        if(len(valList)==2):
            pprice = valList[1]
            perchange = round((((float(tprice)/float(pprice))-1)*100), 2)
            if(perchange>0):
                perchange = "+"+str(perchange)
            else:
                perchange = str(perchange)

            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.purple(),
                    title = "Trim: "+valList[0]+" shares at "+tprice+" from "+pprice+" ("+perchange+"%)",
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.purple(),
                    title = "Trim: "+valList[0]+" shares at "+tprice+" from "+pprice+" ("+perchange+"%)",
                    timestamp = datetime.utcnow()
                )
            valList = ["Trim: "+str(valList[0]), pprice, tprice, perchange]
        else:
            pprice = valList[3]
            perchange = round((((float(tprice)/float(pprice))-1)*100), 2)
            if(perchange>0):
                perchange = "+"+str(perchange)
            else:
                perchange = str(perchange)

            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.purple(),
                    title = "Trim: "+valList[0]+" "+valList[1]+" "+valList[2]+" at "+tprice+" from "+pprice+" ("+perchange+"%)",
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.purple(),
                    title = "Trim: "+valList[0]+" "+valList[1]+" "+valList[2]+" at "+tprice+" from "+pprice+" ("+perchange+"%)",
                    timestamp = datetime.utcnow()
                )
            valList = ["Trim: "+str(valList[0]), valList[1], valList[2], pprice, tprice, perchange]
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)
        todtrades.append(valList)
        wtrades.append(valList)

@bot.command()
async def fix(ctx, id, ticker, strike, exp, pprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        ticker = ticker.upper()
        strike = strike.upper()
        valList = [ticker, strike, exp, pprice]
        if(comment!=None):
            embed = discord.Embed(
                colour = discord.Colour.gold(),
                title = "Edit: "+ticker+" "+strike+" "+exp+" at "+pprice,
                description = "```"+comment+"```",
                timestamp = datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                colour = discord.Colour.gold(),
                title = "Edit: "+ticker+" "+strike+" "+exp+" at "+pprice,
                timestamp = datetime.utcnow()
            )
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)
        otrades[int(id)-1] = valList
        await ctx.send("Edited!")

@bot.command()
async def average(ctx, id, pprice, *, comment=None):
    if(ctx.channel.id == cmdChannelId):
        valList = otrades[int(id)-1]
        if(len(valList)==2):
            otrades[int(id)-1][1] = pprice
            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.gold(),
                    title = "Average: "+valList[0]+" shares to "+pprice,
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.gold(),
                    title = "Average: "+valList[0]+" shares to "+pprice,
                    timestamp = datetime.utcnow()
                ) 
        else:
            otrades[int(id)-1][3] = pprice
            if(comment!=None):
                embed = discord.Embed(
                    colour = discord.Colour.gold(),
                    title = "Average: "+valList[0]+" "+valList[1]+" "+valList[2]+" to "+pprice,
                    description = "```"+comment+"```",
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    colour = discord.Colour.gold(),
                    title = "Average: "+valList[0]+" "+valList[1]+" "+valList[2]+" to "+pprice,
                    timestamp = datetime.utcnow()
                )
        embed.set_footer(text = "ID: "+str(id))
        await embedSend(embed)

@bot.command()
async def open(ctx):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "**Open Positions**",
            timestamp = datetime.utcnow()
        )
        for i in range(len(otrades)):
            valList = otrades[i]
            if(valList == 0):
                pass
            else:
                if(len(valList)==2):
                    embed.add_field(name = "ID: "+str(i+1), value = valList[0]+" shares at "+valList[1], inline = False)
                else:
                    embed.add_field(name = "ID: "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[3], inline = False)
            if(i>24):
                embed2 = discord.Embed(
                    colour = discord.Colour.blue(),
                    title = "**Open Positions Cont.**",
                    timestamp = datetime.utcnow()
                )
                for j in range(25, len(otrades)):
                    valList = otrades[j]
                    if(valList == 0):
                        pass
                    else:
                        if(len(valList)==2):
                            embed2.add_field(name = "ID: "+str(j+1), value = valList[0]+" shares at "+valList[1], inline = False)
                        else:
                            embed2.add_field(name = "ID: "+str(j+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[3], inline = False)
                continue
        for i in range(len(serverList)):
            currentServer = serverList[i]
            guild = bot.get_guild(currentServer[0])
            channel = bot.get_channel(currentServer[1])
            if(currentServer[2]!=0):
                role = get(guild.roles, id=currentServer[2])
                send = await channel.send(f"{role.mention} @everyone",embed = embed)
            else:
                send = await channel.send("@everyone",embed = embed)
            if(currentServer[1]==765777392777691188):
                await send.add_reaction("<a:acegif:796407661830340688>")
            elif(currentServer[1]==808534558819090482):
                await send.add_reaction("✅")
            if(embed2 != None):
                send = await channel.send(embed=embed2)
                if(currentServer[1]==765777392777691188):
                    await send.add_reaction("<a:acegif:796407661830340688>")
                elif(currentServer[1]==808534558819090482):
                    await send.add_reaction("✅")

@bot.command()
async def openhere(ctx):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "**Open Positions**",
            timestamp = datetime.utcnow()
        )
        for i in range(len(otrades)):
            valList = otrades[i]
            if(valList == 0):
                pass
            else:
                if(len(valList)==2):
                    embed.add_field(name = "ID: "+str(i+1), value = valList[0]+" shares at "+valList[1], inline = False)
                else:
                    embed.add_field(name = "ID: "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[3], inline = False)
            if(i>24):
                embed2 = discord.Embed(
                    colour = discord.Colour.blue(),
                    title = "**Open Positions Cont.**",
                    timestamp = datetime.utcnow()
                )
                for j in range(25, len(otrades)):
                    valList = otrades[j]
                    if(valList == 0):
                        pass
                    else:
                        if(len(valList)==2):
                            embed2.add_field(name = "ID: "+str(j+1), value = valList[0]+" shares at "+valList[1], inline = False)
                        else:
                            embed2.add_field(name = "ID: "+str(j+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[3], inline = False)
                continue
        await ctx.channel.send(embed = embed)
        if(embed2 != None):
            await ctx.channel.send(embed = embed2)

@bot.command()
async def clopen(ctx, id):
    if(ctx.channel.id == cmdChannelId):
        if(id != None):
            otrades.pop(int(id)-1)
            await ctx.send("Cleared Trade "+id+"!")

@bot.command()
async def ttrades(ctx):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "**Today's Trades**",
            timestamp = datetime.utcnow()
        )
        for i in range(len(todtrades)):
            valList = todtrades[i]
            if(len(valList) == 1):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" shares (Stopped out)", inline = False)
            elif(len(valList) == 3):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" (Stopped out)", inline = False)
            elif(len(valList) == 4):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" shares at "+valList[2]+" from "+valList[1]+ " ("+valList[3]+"%)", inline = False)
            else:
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[4]+" from "+valList[3]+" ("+valList[5]+"%)", inline = False)
        await embedSend(embed)

@bot.command()
async def clttrades(ctx, id=None):
    if(ctx.channel.id == cmdChannelId):
        if(id != None):
            todtrades.pop(int(id)-1)
            await ctx.send("Cleared Trade "+id+"!")
        else:
            todtrades.clear()
            await ctx.send("Cleared Today's Trades!")

@bot.command()
async def wr(ctx):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "**This Weeks's Trades**",
            timestamp = datetime.utcnow()
        )
            
        for i in range(len(wtrades)):
            valList = wtrades[i]
            if(len(valList) == 1):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" shares (Stopped out)", inline = False)
            elif(len(valList) == 3):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" (Stopped out)", inline = False)
            elif(len(valList) == 4):
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" shares at "+valList[2]+" from "+valList[1]+ " ("+valList[3]+"%)", inline = False)
            else:
                embed.add_field(name = "Trade "+str(i+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[4]+" from "+valList[3]+" ("+valList[5]+"%)", inline = False)
            if(i>24):
                embed2 = discord.Embed(
                    colour = discord.Colour.blue(),
                    title = "**This Weeks's Trades Cont.**",
                    timestamp = datetime.utcnow()
                )
                for j in range(25, len(wtrades)):
                    valList = wtrades[j]
                    if(len(valList) == 1):
                        embed.add_field(name = "Trade "+str(j+1), value = valList[0]+" shares (Stopped out)", inline = False)
                    elif(len(valList) == 3):
                        embed.add_field(name = "Trade "+str(j+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" (Stopped out)", inline = False)
                    elif(len(valList) == 4):
                        embed.add_field(name = "Trade "+str(j+1), value = valList[0]+" shares at "+valList[2]+" from "+valList[1]+ " ("+valList[3]+"%)", inline = False)
                    else:
                        embed.add_field(name = "Trade "+str(j+1), value = valList[0]+" "+valList[1]+" "+valList[2]+" at "+valList[4]+" from "+valList[3]+" ("+valList[5]+"%)", inline = False)
                continue
        for i in range(len(serverList)):
            currentServer = serverList[i]
            guild = bot.get_guild(currentServer[0])
            channel = bot.get_channel(currentServer[1])
            if(currentServer[2]!=0):
                role = get(guild.roles, id=currentServer[2])
                send = await channel.send(f"{role.mention} @everyone",embed = embed)
            else:
                send = await channel.send("@everyone",embed = embed)
            if(currentServer[1]==765777392777691188):
                await send.add_reaction("<a:acegif:796407661830340688>")
            elif(currentServer[1]==808534558819090482):
                await send.add_reaction("✅")
            if(embed2 != None):
                send = await channel.send(embed=embed2)
                if(currentServer[1]==765777392777691188):
                    await send.add_reaction("<a:acegif:796407661830340688>")
                elif(currentServer[1]==808534558819090482):
                    await send.add_reaction("✅")

@bot.command()
async def clwr(ctx, id=None):
    if(ctx.channel.id == cmdChannelId):
        if(id != None):
            wtrades.pop(int(id)-1)
            await ctx.send("Cleared WTrade "+id+"!")
        else:
            wtrades.clear()
            await ctx.send("Cleared this Weeks's Trades!")

@bot.command()
async def comment(ctx, *, message):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = "```"+message+"```",
            timestamp = datetime.utcnow()
        ) 
        await embedSend(embed)

@bot.command()
async def image(ctx, *, message=None):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    if(message!=None):
        embed.set_image(url=message)
    else:
        embed.set_image(url=ctx.message.attachments[0].url)
    await embedSend(embed)

@bot.command()
async def polltoday(ctx):
    if(ctx.channel.id == cmdChannelId):
        guild = bot.get_guild(764264878755020850)
        channel = bot.get_channel(765776867901964291)
        premium = get(guild.roles, id=784629373571301397)
        embed = discord.Embed(
            colour = discord.Colour.from_rgb(255, 110, 199),
            title = "How was your trading today?",
            description = "🟢Profit\n🔴Lost\n🟡Break even\n🏖️Sat back"
        )
        message = await channel.send(f"{premium.mention} @everyone",embed = embed)
        await message.add_reaction("🟢")
        await message.add_reaction("🔴")
        await message.add_reaction("🟡")
        await message.add_reaction("🏖️")

@bot.command()
async def cl(ctx):
    await ctx.channel.purge()

@bot.command()
async def help(ctx):
    if(ctx.channel.id == cmdChannelId):
        embed = discord.Embed(
            colour = discord.Colour.orange(),
            title = "**Commands**",
        )
        embed.add_field(name = "/BTO", value = "Send a buy alert for an option: /BTO (ticker) (50c or 50p) (expiration) (purchasePrice) (comment)", inline=False)
        embed.add_field(name = "/STC", value = "Send a sell alert for an option: /STC (id) (sellPrice) (comment)", inline=False)
        embed.add_field(name = "/LoadBTO", value = "Add to list of open trades without an alert: /BTO (ticker) (50c or 50p) (expiration) (purchasePrice) (comment)", inline=False)
        embed.add_field(name = "/LoadSTC", value = "Sell without an alert: /STC (id) (sellPrice) (comment)", inline=False)
        embed.add_field(name = "/BS", value = "Send a buy alert for shares: /BS (ticker) (price) (comment)", inline=False)
        embed.add_field(name = "/SS", value = "Send a sell alert for shares: /SS (id) (sellPrice) (comment)", inline=False)
        embed.add_field(name = "/cut", value = "Send a cut alert when your SL is hit: /cut (id) (comment)", inline=False)
        embed.add_field(name = "/update", value = "Alert an update on the trade: /update (id) (comment)", inline=False)
        embed.add_field(name = "/trim", value = "Alert a trim on the trade: /update (id) (trim price) (comment % of position)", inline=False)
        embed.add_field(name = "/fix", value = "Use to fix a position if a mistake was made: /fix (id) (ticker) (50c or 50p) (expiration) (purchasePrice) (comment)", inline=False)
        embed.add_field(name = "/average", value = "Use to average the price of a position: /average (id) (newPrice) (comment)", inline=False)
        embed.add_field(name = "/open", value = "Clears the id of the open trade you pick: /clopen (id)", inline=False)
        embed.add_field(name = "/clopen", value = "Sends your open trades in the alert chat", inline=False)
        embed.add_field(name = "/openhere", value = "Sends your open trades in the command chat", inline=False)
        embed.add_field(name = "/ttrades", value = "Sends today's closed trades", inline=False)
        embed.add_field(name = "/clttrades", value = "Clears today's closed trades, make sure to do this either before or after each trading day", inline=False)
        embed.add_field(name = "/wr", value = "Sends this week's closed trades", inline=False)
        embed.add_field(name = "/clwr", value = "Clears this week's closed trades", inline=False)
        embed.add_field(name = "/comment", value = "Send a comment like this: /comment (the comment itself)", inline=False)
        embed.add_field(name = "/image", value = "Send a image like this: /comment (url) **or like this** /comment (attach an image)", inline=False)
        embed.add_field(name = "/polltoday", value = "Send out a poll about the trading day!", inline=False)
        embed.add_field(name = "/info", value = "This is for @Hima when he needs to push new code, just to track current trades so they are not lost.", inline=False)
        embed.add_field(name = "**NOTE**", value = "cut, update, trim, and average work for both options and shares, but not edit.", inline=False)
        await ctx.send(embed = embed)

bot.run('//paste in bot id')