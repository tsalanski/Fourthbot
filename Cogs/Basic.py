#############
## Basic.py
## Author: Chris Scaramella and Brian Scaramella
## Date: 5/15/2019
## Testing out cogs and commands.  This file will be archived during the switch to v2.0
#############
import discord
from discord.ext import commands

import logging
import random
import re
from datetime import datetime

# Magic Variables
UNOOF_PERCENT = 2
B_OOF_PERCENT = 20
OOF_RESPONSES = ["Big oof, my dudes", 
    "Aw fuck I can't believe you done this",
    "I'm not even surprised tbh", 
    "I am dead :joy::joy::joy:",
    ""
    '"Bitchy Bic Bickerson" -Alyssa Knight', 
    "I am confusion",
    "You tried", 
    "May I ask why you need this crowdsourcing data?", 
    "Good job team. This is what I've come to expect from you.",
    "OOF ||Test||", 
    "What does this question mean?",]
OOF_RESPONSES_P = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100]

def setup(bot):
    bot.add_cog(Basic(bot))

class Basic(commands.Cog):
    """ All basic commands that don't require any other handlers can be found here."""
    def __init__(self,bot):
        self.bot = bot
        logging.debug("Basic Cog loaded")
        random.seed(datetime.now())

    @commands.command(help="Say hello to the bot.")
    async def hi(self, ctx):
        msg = "Hello {0.message.author.mention}".format(ctx)
        await ctx.send(msg)
    
    #TODO: Find a better way to update the about command
    @commands.command(help="About this bot")
    async def about(self, ctx):
        msg = ("I am FourthBot v2.1.  I act as the 4th DM for the group.  You can ask "
            "me lots of things or use me to roll dice through discord, or use me to "
            "keep track of your characters, experience, spells, and treasure.  I am not "
            "finished yet though!  Use !help to see all of my current commands.")
        await ctx.send(msg)

    #TODO: Clarify oof command - Brian
    @commands.command(help="For those oofs that are bound to happen")
    async def oof(self, ctx):
        msg = random.choices(OOF_RESPONSES, weights=OOF_RESPONSES_P)[0]
        r = random.random()
        if r < UNOOF_PERCENT/100.0:
            msg = (msg[0:10] + "... No... You know what? Not this time. I am rewinding time "
                "to right before whatever "
                "caused this oof. Don't waste this moment of generosity. **UN:clap:OOF:clap:**")
        elif (r-UNOOF_PERCENT/100.0) < B_OOF_PERCENT/100.0:
            msg = msg.replace('b', ':b:')
            msg = msg.replace('B', ':b:')
        await ctx.send(msg)
    
    #TODO: Add more syntax to roll command, and make it cleaner (maybe add a separate roll function?)
    @commands.command(help="Roll dice how you would see the dice written (XdX)")
    async def roll(self, ctx):
        words = ctx.message.content.split()
        sum_value = 0
        if len(words) == 1:
            msg = ("Roll dice how you would see the dice written\n"
                    "Examples: **!roll d20** : roll 1 d20\n"
                    "**!roll 8d6** : roll 8 d6s \n"
                    "**!roll 1d20 2d12 3d8**")
            await ctx.send(msg)
        if len(words) == 2 and words[1]=='character':
            words = ['!roll', '4d6', '4d6', '4d6', '4d6', '4d6', '4d6']
            sum_value = 3
        output = []
        for die in words[1:]:
            matchObj = re.match(r'(\d*)d(\d+)', die)
            if matchObj == None: continue
            if matchObj.group(1) == '':
                quantity = 1
            else:
                quantity = int(matchObj.group(1))
            if quantity > 100: quantity = 100
            die_size = int(matchObj.group(2))
            if die_size < 2: die_size = 2
            if die_size > 100: die_size = 100
            rolls = []
            for i in range(quantity):
                rolls.append(random.randint(1,die_size))
            output.append(rolls)
            
            out_string = ''
            group_sums = 0
        for group in output:
            if sum_value == 0:
                out_string = out_string + '[' + ','.join(map(str,group)) + ']' +'(' + str(sum(group)) + ')'
                group_sums = group_sums + sum(group)
            else:
                group.sort(reverse=True)
                out_string = out_string + '[' + ','.join(map(str,group)) + ']' +'(' + str(sum(group[0:sum_value])) + ')'
        out_string = out_string + ' =' +str(group_sums)
        await ctx.send(out_string)

    @commands.command(help="Tell Fourthbot your discord ID number so we can track it.")
    async def gattaca(self, ctx):
        print(ctx.message.author.id)
        print(ctx.message.channel.id)
        await ctx.send("Thank you!")
