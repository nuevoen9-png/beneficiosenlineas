import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Configuración de FastAPI
app = FastAPI()

# Configuración del Bot de Discord
TOKEN = os.getenv("DISCORD_TOKEN", "MTU1NDkxNTk3Nzg1NzIwNDI1NQ.G72umO.NeBPxli9X-JLq7hRsDUkURlrXzsD2vHntSlr9M")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "1570766356016664676"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

class MensajeData(BaseModel):
    mensaje: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Beneficios en Línea</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; color: #333; }
                h1 { color: #2c3e50; }
                p { font-size: 18px; }
                .container { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Bienvenido a Beneficios en Línea!</h1>
                <p>La página web y el servicio de Discord están funcionando correctamente.</p>
                <p><strong>Estado:</strong> En línea y operativo 🚀</p>
            </div>
        </body>
    </html>
    """

@app.post("/send")
def send_message(data: MensajeData):
    try:
        future = asyncio_run_coro(send_to_discord(data.mensaje))
        return {"status": "success", "message": "Mensaje enviado a Discord"}
    except Exception as e:
        raise HTTPException(status_code=500, str(e))

async def send_to_discord(text: str):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(text)

def run_bot():
    bot.run(TOKEN)

# Iniciar el bot de Discord en segundo plano al arrancar FastAPI
threading.Thread(target=run_bot, daemon=True).start()
