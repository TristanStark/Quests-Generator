import logging
import os
from collections.abc import Iterable

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from .exporter_runner import run_exporter


def _parse_guild_ids(raw: str | None) -> Iterable[int]:
    if not raw:
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip()]




def create_bot() -> commands.Bot:
    load_dotenv()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
    logger = logging.getLogger(__name__)


    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)


    guild_ids = _parse_guild_ids(os.getenv("GUILD_IDS"))


    @bot.event
    async def on_ready():
        logger.info("✅ Connecté en tant que %s", bot.user)
        try:
            if guild_ids:
                synced = []
                for gid in guild_ids:
                    g = discord.Object(id=gid)
                    synced.extend(await bot.tree.sync(guild=g))
            else:
                synced = await bot.tree.sync()
                logger.info("✅ %d commandes slash synchronisées.", len(synced))
        except Exception as e: # noqa: BLE001
            logger.exception("[ERROR] Erreur de sync : %s", e)


    @bot.tree.command(name="quetes", description="Génère une quête depuis un synopsis")
    @app_commands.describe(synopsis="Le synopsis de la quête à générer")
    async def quetes(interaction: discord.Interaction, synopsis: str):
        logger.info("🔍 /quetes synopsis=%s", synopsis)
        await interaction.response.defer()
        await interaction.followup.send(
        "[WAITING] Génération de la quête en cours... (jusqu’à ~30s)",
        ephemeral=True,
    )

        result = run_exporter(synopsis)
        if result.returncode != 0:
            msg = result.stderr.strip() or "Erreur inconnue"
            await interaction.followup.send(f"[ERROR] Erreur :\n```\n{msg[:1900]}\n```")
        else:
            msg = result.stdout.strip() or "[SUCCESS] Script terminé sans sortie."
            await interaction.followup.send(f"[RESULT] Résultat :\n```\n{msg[:1900]}\n```")

    return bot




def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN manquant (voir .env.example)")

    bot = create_bot()
    bot.run(token)




if __name__ == "__main__":
    main()
