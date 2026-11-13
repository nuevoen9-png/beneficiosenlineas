import os
import asyncio
import discord
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@app.on_event("startup")
async def startup_event():
    async def run_bot():
        try:
            await bot.start(TOKEN)
        except Exception as e:
            print(f"Error al iniciar el bot: {e}")
    
    asyncio.create_task(run_bot())

@app.post("/send")
async def send_json(data: dict):
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Discord bot is not ready")
    
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        raise HTTPException(status_code=404, detail="Discord channel not found")
    
    message_text = data.get("message", "Hola")
    await channel.send(message_text)
    return {"status": "success", "message": message_text}