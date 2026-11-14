import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Montar los archivos estáticos de la compilación de React (si existe la carpeta dist/build)
# O servir directamente el index.html de tu proyecto
@app.get("/")
def serve_index():
    index_path = "react-tailwind/dist/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    # Ruta alternativa si los archivos están en la raíz de react-tailwind
    elif os.path.exists("react-tailwind/index.html"):
        return FileResponse("react-tailwind/index.html")
    return {"message": "¡Proyecto sincronizado! Falta compilar React en Render."}

# Si tienes archivos estáticos de assets (js, css)
if os.path.exists("react-tailwind/dist"):
    app.mount("/assets", StaticFiles(directory="react-tailwind/dist/assets"), name="assets")

@app.post("/send")
def send_message(data: MensajeData):
    try:
        return {"status": "success", "message": "Datos recibidos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_bot():
    bot.run(TOKEN)

threading.Thread(target=run_bot, daemon=True).start()
