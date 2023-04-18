"""

This code creates the dictionary file and logs messages sent over Discord as input

DISCLAIMER: this code is also very messy but it works :)

"""


from discord.ext import commands
import discord
import os
import json
import sys
from asciiMarkov import asciiMarkov
print(asciiMarkov)


client = discord.Client(intents=discord.Intents.all())

TOKEN =  # paste Discord bot token here


@client.event
async def on_connect():
    print("nMarkov connected to server.")


@client.event
async def on_ready():   # just for the funny
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Detroit: Become Human'))


# this logs messages into the dictionary
@client.event
async def on_message(message):  # activates when a message is sent in Discord
    # separates username from id numbers
    username = str(message.author).split('#')[0]
    user_message = str(message.content)

    dictionaryFile = readArguments()
    dictionary = loadDictionary(dictionaryFile)

    try:
        # if sent by markov, ignore
        if message.author == client.user:
            return

        # change guild ID based on which server markov listens to
        if message.guild.id ==  # guild ID:
            # prints the logged message into terminal
            print(f'{username}: {user_message}')
            content = (f'{user_message}')

            # adds message content into dictionary
            dictionary = learn(dictionary, content)
            updateFile(dictionaryFile, dictionary)

        else:
            pass
    except:
        pass


def readArguments():
    dictionaryFile = "dictionary.json"     # dictionary file name to write into
    return dictionaryFile


def loadDictionary(filename):   # loads the dictionary based on filename arg
    if not os.path.exists(filename):    # checks if the file exists, must be .json format
        # creates a new dictionary file with name specified if not found
        file = open(filename, "w")
        json.dump({}, file)  # writes empty text into it
        file.close()

    file = open(filename, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary


def learn(dict, input):     # splits up logged messages into individual words, writes into dictionary
    tokens = input.split(" ")
    for i in range(0, len(tokens)-1):
        currentWord = tokens[i]
        nextWord = tokens[i+1]

        if currentWord not in dict:
            # create new entry in dictionary
            dict[currentWord] = {nextWord: 1}
        else:
            # current word already in dictionary
            allNextWords = dict[currentWord]

            if nextWord not in allNextWords:
                # add new text state
                dict[currentWord][nextWord] = 1
            else:
                # already exists, just increment
                dict[currentWord][nextWord] = dict[currentWord][nextWord] + 1
    return dict


def updateFile(filename, dictionary):
    file = open(filename, "w")
    json.dump(dictionary, file)
    file.close


dictionaryFile, inputFile = readArguments()
dictionary = loadDictionary(dictionaryFile)


client.run(TOKEN)
