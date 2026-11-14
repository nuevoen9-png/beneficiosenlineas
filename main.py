import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

TOKEN = os.getenv("DISCORD_TOKEN", "MTU1NDkxNTk3Nzg1NzIwNDI1NQ.G72umO.NeBPxli9X-JLq7hRsDUkURlrXzsD2vHntSlr9M")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "157076635601664676"))

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
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beneficios en Línea</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; color: #333; }
            .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); text-align: center; max-width: 400px; width: 100%; }
            h1 { color: #2d3748; margin-bottom: 15px; font-size: 24px; }
            p { color: #4a5568; font-size: 16px; line-height: 1.5; }
            .badge { display: inline-block; background: #c6f6d5; color: #22543d; padding: 6px 12px; border-radius: 20px; font-weight: bold; margin-top: 15px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido a Beneficios en Línea!</h1>
            <p>Tu plataforma web y el sistema de notificaciones de Discord se encuentran sincronizados y listos.</p>
            <div class="badge">🚀 Sistema Operativo</div>
        </div>
    </body>
    </html>
    """

@app.post("/send")
def send_message(data: MensajeData):
    try:
        return {"status": "success", "message": "Datos recibidos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_bot():
    bot.run(TOKEN)

threading.Thread(target=run_bot, daemon=True).start()
