import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import subprocess
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SCRIPT_PATH = r"H:\github\Projet Impérial 4\exporter.py"
SCRIPT_DIRECTORY = r"H:\github\Projet Impérial 4"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"❌ Erreur de sync : {e}")

def run_exporter(synopsis: str):
    cmd = ["python", SCRIPT_PATH, "--synopsis", synopsis]
    return subprocess.run(cmd, cwd=SCRIPT_DIRECTORY, capture_output=True, text=True)


@bot.tree.command(name="quetes", description="Génère une quête depuis un synopsis")
@app_commands.describe(synopsis="Le synopsis de la quête à générer")
async def quetes(interaction: discord.Interaction, synopsis: str):
    print(f"🔍 Commande /quetes appelée avec le synopsis : {synopsis}")
    await interaction.response.defer()  # en cas de délai
    msg = await interaction.followup.send("⏳ Génération de la quête en cours... (cela peut prendre jusqu’à 30 secondes)")
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, run_exporter, synopsis)

    if result.returncode != 0:
        msg = result.stderr.strip() or "Erreur inconnue"
        await interaction.followup.send(f"❌ Erreur lors de la génération :\n```\n{msg[:1900]}\n```")
    else:
        msg = result.stdout.strip() or "✅ Script terminé sans sortie."
        await interaction.followup.send(f"🧾 Résultat :\n```\n{msg[:1900]}\n```")

bot.run(TOKEN)
