import discord
import requests
import json
import random
# settings.py
from dotenv import load_dotenv
import os 
from nlp_analyze import get_sentiment_score 
from scrape_word import get_random_happy_word, get_random_sad_word
import pymongo
from pymongo import MongoClient
import urllib
import uuid

# load
load_dotenv()
# Env vars
SECRET_KEY = os.getenv("token")
TENOR_KEY = os.getenv("tenorkey")

client = discord.Client()
mongo_uri = "mongodb+srv://qhackteam2021:" + urllib.parse.quote("Password@123") + "@mycluster.7ok43.mongodb.net/test"
cluster = MongoClient(mongo_uri)
# cluster = MongoClient("mongodb+srv://qhackteam2021:Password@123@mycluster.7ok43.mongodb.net/test")
db = cluster["mydatabase"]
collection = db["qhacks"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(''):
        vals = message.content.split(" ")
        mood = get_sentiment_score(" ".join(vals))
        author = message.author
        timestamp = message.created_at
        channel = message.channel.id
        
        
        post = {"_id": uuid.uuid4(), "author": message.author.id, "score": 1}
        collection.insert_one(post)
        await message.channel.send('accepted!')


        if mood < 0:
            search_term = get_random_happy_word()
        else: 
            search_term = get_random_sad_word()
        r = requests.get("https://api.tenor.com/v1/random?q=%s&key=%s&limit=1" % (search_term, TENOR_KEY))
        parsed = json.loads(r.content)
        good = parsed['results'][0]['media'][0]['tinygif']['url']
        await message.channel.send(good)
        await message.channel.send(search_term)
        await message.channel.send("%s %s %s %s" % (author, mood, timestamp, channel))
        # post = {"_id": author, "mood": mood, "timestamp": timestamp, "channel": channel}
        # collection.insert_one(post)
        # await message.channel.send('accepted!')
        # await savetodb(message, author, mood, timestamp, channel)


# async def savetodb(message, author, mood, timestamp, channel):
#     post = {"_id": author, "mood": mood, "timestamp": timestamp, "channel": channel}
#     collection.insert_one(post)
#     await message.channel.send('accepted!')


client.run(SECRET_KEY)