"""

This code creates the text generation function (def main()) and dictionary file (loadDictionary())
Also sets up Discord compatibility & 24/7 server hosting via Hikari

DISCLAIMER: this code is very messy but it works :)

"""


from discord.ext import commands
import discord
import sys
import os.path
import os
import json
import random
import hikari
import lightbulb

bot = lightbulb.BotApp(
    token=# paste Discord bot token here
)

client = discord.Client(intents=discord.Intents.all())

# clarify the bot token
TOKEN =  # paste discord bot token here


def main():     # generates message based on data from other funcs
    length, filename = readArguments()
    dictionary = loadDictionary(filename)

    lastWord = "~~~~~~~~~~~~~~~"    # random stuff to generate random new word as start
    result = ""
    for i in range(0, length):  # where the magic happens
        newWord = getNextWord(lastWord, dictionary)
        result = result + " " + newWord
        lastWord = newWord

    print(result)


def readArguments():    # could be a cmd prompt but im lazy
    length = 25     # this argument changes the length of the generated text, value represents the number of words printed
    filename = "dictionary.json"   # arg to set the dictionary to read words from

    numArguments = len(sys.argv) - 1
    if numArguments >= 1:
        length = int(sys.argv[1])
    if numArguments >= 2:
        filename = sys.argv[2]

    return length, filename


def loadDictionary(filename):   # loads the dictionary based on filename arg from readArguments()
    if not os.path.exists(filename):    # checks if the dictionary file exists
        sys.exit("Error: Dictionary file not found")

    filename = # dictionary file to read from i.e. "dictionary.json"
    file = open(filename, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary


def getNextWord(lastWord, dict):    # used during generation process to pick words based on Markov chain
    if lastWord not in dict:
        # pick new random state
        newWord = pickRandom(dict)
        return newWord

    else:
        # pick next word from list
        potentialWord = dict[lastWord]
        potentialNormalized = []

        for word in potentialWord:
            freq = potentialWord[word]
            for i in range(0, freq):
                potentialNormalized.append(word)

        rnd = random.randint(0, len(potentialNormalized)-1)
        return potentialNormalized[rnd]


def pickRandom(dict):   # picks a random number which corresponds to a word in the dictionary, used as first word in message generation
    randNum = random.randint(0, len(dict)-1)
    newWord = list(dict.keys())[randNum]
    return newWord


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('nMarkov v2 is online!')  # prints into terminal bot starts up


@bot.command
@lightbulb.command('speakup', 'Let the man speak his mind.')    # sets the name of the command and it's description
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):    # activated when /speakup command is used
    length, filename = readArguments()
    dictionary = loadDictionary(filename)

    lastWord = "~~~~~~~~~~~~~~~"    # random text, starts generation with random word
    result = ""
    for i in range(0, length):  # text time
        newWord = getNextWord(lastWord, dictionary)
        result = result + " " + newWord
        lastWord = newWord

    await ctx.respond(result + " " + "daddy")   # sends message


"""
    At one point I wrote some stuff to set up a system that'd have him randomly send a message (didnt really work),
    I haven't really touched this code in a minute so i'm just gonna leave it as is
"""
@client.event
async def on_message(message):
    print('message detected')
    # if sent by markov, ignore
    if message.author == client.user:
        return

    # change guild ID based on which server markov listens to
    elif message.guild.id == """insert guild ID here""":
        chance = random.randint(1, 100)
        if chance <= 50:
            length, filename = readArguments()
            dictionary = loadDictionary(filename)

            lastWord = "~~~~~~~~~~~~~~~"
            result = ""
            for i in range(0, length):
                newWord = getNextWord(lastWord, dictionary)
                result = result + " " + newWord
                lastWord = newWord

            await ctx.respond(result + " " + "daddy")
        else:
            pass
    else:
        pass


bot.run()
