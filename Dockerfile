# Étape 1 : base
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /app


# Copier le projet
COPY pyproject.toml README.md ./
COPY src ./src


# Installer en mode app
RUN pip install --upgrade pip && pip install .[dev]


# Dossier externe (où vit exporter.py)
# Monte ton dossier réel à l'exécution: -v /chemin/vers/exporter:/app/external
RUN mkdir -p /app/external /app/data


# Exécuter le bot
ENV LOG_LEVEL=INFO
CMD ["python", "-m", "quest_generator_bot.bot"]