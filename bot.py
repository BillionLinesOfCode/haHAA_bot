import os
import discord, json # Import discord and json modules
from dotenv import load_dotenv
from discord.ext import commands
from openai import OpenAI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')
GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_URL = os.getenv('GROK_API_URL')

intents = discord.Intents.default()
intents.message_content = True
grok_client = OpenAI(
    api_key=GROK_API_KEY,
    base_url=GROK_URL
)
client  = commands.Bot(command_prefix=PREFIX, intents=intents) 


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@client.command()
async def grok(ctx, *, question):
    completion = grok_client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {"role": "system", "content": "You are Grok, a  know-all chatbot that is answering questions from discord users. Keep responces as breif as possible. no extra wording in responces if an image is requested"},
            {"role": "user", "content": question},
        ],
    )
    await ctx.reply(completion.choices[0].message.content)

# This code can be enabled when grok API is updated for image generation
# @client.command()
# async def image(ctx, *, description):
#     image_responce = grok_client.images.generate(
#         prompt=description,
#         n=1,
#         size="1024x1024"
#     )
#     image_url = image_responce['data'][0]['url']
#     await ctx.reply(image_url)

client.run(TOKEN)