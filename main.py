import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Token directo para asegurar que arranque sin problemas
TOKEN = "MTU1NDkxNTk3N3k1NzEwNzIwNDQ5.G72umO.NeBPxli9X-JLq7hsDUKUlRXzsD2vHntSlr9M"
CHANNEL_ID_STR = os.getenv("DISCORD_CHANNEL_ID", "157076635601664676")
CHANNEL_ID = int(CHANNEL_ID_STR) if CHANNEL_ID_STR else None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado exitosamente como {bot.user}")

class MensajeData(BaseModel):
    mensaje: str

# Interfaz visual web profesional con Tailwind CSS
@app.get("/", response_class=HTMLResponse)
def serve_index():
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
            <p class="text-gray-300 mb-6">Tu plataforma web y el bot de Discord se encuentran sincronizados y operativos.</p>
            <div class="bg-gray-900 p-4 rounded-lg border border-gray-700 text-green-400 font-mono text-sm">
                Estado: En línea y funcionando 🚀
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/send")
def send_message(data: MensajeData):
    try:
        return {"status": "success", "message": "Datos procesados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_bot():
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Token de Discord no configurado.")

# Hilo en segundo plano para ejecutar el bot de Discord junto con FastAPI
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
