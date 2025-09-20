import subprocess
import types

from quest_generator_bot.bot import create_bot
from quest_generator_bot.exporter_runner import run_exporter


def test_create_bot_smoke(monkeypatch):
    # Pas besoin de token pour juste construire l'objet
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    bot = create_bot()
    assert hasattr(bot, "tree")




def test_run_exporter_builds_command(monkeypatch):
    # On remplace subprocess.run par un double qui capture les arguments
    captured = {}


    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        # Simule un succès
        cp = types.SimpleNamespace(returncode=0, stdout="OK", stderr="")
        return cp


    monkeypatch.setenv("SCRIPT_PATH", "/tmp/exporter.py")
    monkeypatch.setenv("SCRIPT_DIRECTORY", "/tmp")
    monkeypatch.setattr(subprocess, "run", fake_run)


    res = run_exporter("Un synopsis")
    assert res.returncode == 0
    assert captured["cwd"] == "/tmp"
    assert captured["cmd"][:2] == ["python", "/tmp/exporter.py"]
