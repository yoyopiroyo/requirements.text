# Importar las librerías necesarias
import discord
from discord.ext import commands, tasks
from flask import Flask # type: ignore
from threading import Thread
import os

# Inicializa el servidor Flask
app = Flask('')

@app.route('/')
def home():
    return "Estoy vivo"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Inicia el bot de Discord
intents = discord.Intents.default()
intents.members = True  # Habilita el intent para manejar los miembros
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

AFK_CHANNEL_ID = 1280347057252728916  # Reemplaza con el ID de tu canal AFK

@bot.event
async def on_ready():
    print(f'Bot {bot.user} ha iniciado sesión.')
    kick_inactive_members.start()  # Inicia la tarea de verificación de miembros inactivos

@tasks.loop(minutes=5)  # Revisa cada 5 minutos
async def kick_inactive_members():
    if bot.guilds:  # Verifica que el bot esté en al menos un servidor
        guild = bot.guilds[0]  # Obtener el primer servidor (guild)
        afk_channel = guild.get_channel(AFK_CHANNEL_ID)  # Obtener el canal AFK

        if afk_channel:
            for member in afk_channel.members:  # Revisa cada miembro en el canal AFK
                try:
                    await member.edit(voice_channel=None)  # Desconecta al miembro
                    print(f'{member.name} ha sido desconectado del canal AFK.')
                except Exception as e:
                    print(f'No se pudo desconectar a {member.name}: {e}')
    else:
        print("El bot no está en ningún servidor.")

# Llama a keep_alive() para mantener el bot vivo
keep_alive()

# Ejecuta el bot de Discord
TOKEN = os.getenv('TOKEN')  # Obtén el token desde una variable de entorno
bot.run(TOKEN)
