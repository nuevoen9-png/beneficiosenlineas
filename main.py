import os
import asyncio
import discord
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Credenciales directas de tus archivos para evitar fallos de entorno en Render
TOKEN = "MTU1NDkxNTk3Nzg1NzIwNDI1NQ.GDP_Xn.3bxBBK7T3KV90ettZsWegv805rFzyZ5bAYxrWI"
CHANNEL_ID = 1570766356952125501

# Interfaz visual de tu proyecto y estado web
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beneficios en Línea</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white min-h-screen flex flex-col items-center justify-center p-6">
        <div class="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700 text-center">
            <h1 class="text-3xl font-extrabold text-blue-400 mb-4">Beneficios en Línea</h1>
            <p class="text-gray-300 mb-6">Tu página web y el bot de Discord se encuentran funcionando y sincronizados.</p>
            <div class="bg-gray-900 p-4 rounded-lg border border-gray-700 text-green-400 font-mono text-sm">
                Estado: ¡Conectado y operativo! 🚀
            </div>
        </div>
    </body>
    </html>
    """

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
