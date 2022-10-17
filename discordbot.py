import discord
from discord.ext import commands
from solonschools import *

TOKEN='no copy me'
bot = commands.Bot(command_prefix="!")

@bot.command()
async def search_staff(ctx, *args):
    if (not args):
        await ctx.send("Do better, not a valid command.")
        return
    # Find all the teachers and info based on input (comes from solonschools.py)
    searchResults = findTeachers(str(' '.join(args))) # ' '.join(args) is to enable spaces in the argument

    # Create a discord embed with the title teachers
    embed = discord.Embed(title="Teachers")
    fieldCounter = 0

    if (searchResults):
        for result in searchResults:
            fieldCounter += 1

            # *Text* will italisize whatever text is between the *
            embed.add_field(name=result["name"], value=f'*{result["building"]}* | *{result["position"]}*', inline=False)

            # Once we hit 25 fields (discord's limit), send this embed out and start a new one if there is more data
            if (fieldCounter == 25 and len(searchResults) > 25):
                fieldCounter = 0
                await ctx.send(embed=embed)
                embed = discord.Embed()
    else:
        # Send error msg that no teacher with the given name exists
        embed.add_field(name="no instance found", value=f'Could not find any teacher with the name: {" ".join(args)}')
    
    await ctx.send(embed=embed)

@bot.command()
async def headline(ctx):
    # Get the most recent headline on solonschool website (from solonschoola.py)
    cHeadline = getHeadline()
    
    # Make an embed to store information in a cleaner way
    embed = discord.Embed(title=cHeadline["header"], url=cHeadline["link"], description=cHeadline["desc"], color=discord.Color.gold())
    embed.set_thumbnail(url=cHeadline["thumbnail"])

    await ctx.send(embed=embed)
bot.run(TOKEN)