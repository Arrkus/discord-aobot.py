import discord
from discord.ext import commands
from discord.utils import get
from datetime import date
import asyncio
import random
import os

bot = commands.Bot(command_prefix='.')

############################################################
## Events ##
@bot.event
async def on_ready():
    '''On startup, the bot gives a confirmation message'''
    print('Booting up...\n.\n..\n...\nThe Alpha Omega bot is online.')




# Errors
@bot.event
async def on_command_error(ctx, error):
    '''Sends an error message'''
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Type ".commands" for a list of commands.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing a required argument. Please pass in all required arguments')




# Reaction Add
@bot.event
async def on_raw_reaction_add(payload):
    '''Assigns a role upon adding a reaction'''
    message_id = 753046698426761338 # The message_id that I want role reaction to
    # ^^ in #rules-and-important-info in AO
    if payload.message_id == message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == "🤷": # Name of emoji
            role = discord.utils.get(guild.roles, name='Bored') # name of role
            role_name = "Bored"
        elif payload.emoji.name == "🏟️": # Name of emoji
            role = discord.utils.get(guild.roles, name='Events')
            role_name = "Events"
        else:
            print(payload.emoji.name)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            role_name = payload.emoji.name

        if role is not None:
            member = discord.utils.get(guild.members, id=payload.user_id)
            if member is not None:
                await member.add_roles(role)
                await member.send(f'''**{guild.name}**: Added role "{role_name}".''')
            else:
                print("Member not found.")
        else:
            print("Role not found.")




# Reaction Remove
@bot.event
async def on_raw_reaction_remove(payload):
    '''Upon removing a reaction, it removes a role'''
    message_id = 753046698426761338 # The message_id that I want role reaction to
    # ^^ in #rules-and-important-info in AO
    if payload.message_id == message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == "🤷": # Name of emoji
            role = discord.utils.get(guild.roles, name='Bored') # name of role
            role_name = "Bored"
        elif payload.emoji.name == "🏟️": # Name of emoji
            role = discord.utils.get(guild.roles, name='Events')
            role_name = "Events"
        else:
            print(payload.emoji.name)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            role_name = payload.emoji.name

        if role is not None:
            member = discord.utils.get(guild.members, id=payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                await member.send(f'''**{guild.name}**: Removed role "{role_name}".''')
            else:
                print("Member not found.")
        else:
            print("Role not found.")




##### Commands ######
# Helpme
@bot.command(aliases=['commands','info'])
async def helpme(ctx):
    ''' Help command '''
    await ctx.channel.send("""
    **Helpful Commands:**```
.help  --> List of commands (Oh, you've already found it)
.ping --> Check latency
```""")
    member = ctx.message.author
    if discord.utils.get(member.roles, name="Management"): # Check if they have a role
        await member.send(f"""**Howdy!** Being apart of Management, you have a few more commands that you will have access to that the others won't. Here are some of them:
        clear <#> --> Clears messages above (# is optional, defaults to 1)
        mute @User <#> <reason> --> Mutes a user for # minutes. (# and reason are optional) Default duration 1 min.
        unmute @User <reason> --> Unmutes a user. Reason is optional
        """)




# Ping
@bot.command()
async def ping(ctx):
    '''Pings the bot and reponds with latency in ms'''
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')




# Clear
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    '''Clears messages in a channel. Only if you can manage messages though'''
    if amount > 5:
        await ctx.send(f"Deleting {amount} messages is alot, keep it 5 or less please.")
        await asyncio.sleep(4)
        await clear(ctx)
    else:
        await ctx.channel.purge(limit=amount)




# Mute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member = None, duration = 1, *, reason=None):
    '''Mutes a user (Assigns @Muted role)'''
    muted = discord.utils.get(ctx.guild.roles, name = 'Muted')
    mutetime = duration * 60
    if member == None:
        await ctx.channel.send('You did not specify anyone to mute.\n The format is: .mute @user <duration (in minutes)> <reason>')
        await asyncio.sleep(10)
        await clear(ctx, 2)
    elif member == ctx.message.author:
        await ctx.channel.send("You can't mute yourself, silly.")
    elif muted in member.roles:
        await clear(ctx)
        await ctx.channel.send(f'"{member.display_name}" is already muted.')
        await asyncio.sleep(2)
        await clear(ctx)
    elif duration < 1:
        await clear(ctx)
        await ctx.send(f'Minimum duration is 1 minute, you entered {duration}')
    else:
        await clear(ctx)
        await member.add_roles(muted,reason=None,atomic=True)
        if reason == None:
            if duration == 1:
                await ctx.channel.send(f'{member.mention} muted for {duration} minute by {ctx.message.author.display_name}.')
            else:
                await ctx.channel.send(f'{member.mention} muted for {duration} minutes by {ctx.message.author.display_name}.')
        elif reason != None:
            if duration == 1:
                await ctx.channel.send(f'{member.mention} muted for {duration} minute by {ctx.message.author.display_name}.\n Reason: {reason}')
            else:
                await ctx.channel.send(f'{member.mention} muted for {duration} minutes by {ctx.message.author.display_name}.\n Reason: {reason}')
        await asyncio.sleep(mutetime)
        if muted in member.roles:
            await unmute(ctx, member)




# Unmute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member = None, *, reason = None):
    '''Unmutes a user (Removes @Muted role)'''
    muted = discord.utils.get(ctx.guild.roles, name = "Muted")
    if member == None:
        await ctx.send('You did not specify anyone to unmute.')
        await asyncio.sleep(2)
        await clear(ctx, 2)
    elif muted not in member.roles:
        await ctx.send(f'"{member.display_name}" isnt muted in the firstplace.')
    elif muted in member.roles:
        await clear(ctx)
        await member.remove_roles(muted,reason=None,atomic=True)
        if reason == None:
            await ctx.channel.send(f'{member.mention} has been unmuted. Welcome back!')
        else:
            await ctx.channel.send(f'{member.mention} has been unmuted by {ctx.message.author.display_name}. Welcome back!\nReason: {reason}')


### Paste from here, up ###

##### Run Bot ######
bot.run(os.environ['token'])
