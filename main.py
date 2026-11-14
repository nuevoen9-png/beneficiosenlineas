import os
import asyncio
import discord
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TOKEN = "MTU1NDkxNTk3Nzg1NzIwNDI1NQ.GDP_Xn.3bxBBK7T3KV90ettZsWegv805rFzyZ5bAYxrWI"
CHANNEL_ID = 1570766356952125501

@app.get("/")
def read_root():
    return {"status": "ok", "message": "¡Mi página y mi bot funcionan en Render!"}

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def run_bot():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

@app.on_event("startup")
def startup_event():
    asyncio.create_task(run_bot())

@app.post("/send")
def send_json(data: dict):
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Discord bot not ready")
    
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        raise HTTPException(status_code=404, detail="Discord channel not found")
        
    return {"status": "sent"}
