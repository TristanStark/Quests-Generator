# Quest Generator Bot

Bot Discord qui génère des quêtes à partir d'un synopsis en appelant un script externe (`exporter.py`) (de base, c'est censé pointer sur le Projet Impérial!).

## 🔎 Fonctionnement
- Slash command `/quetes synopsis:"..."`.
- Le bot appelle `exporter.py --synopsis "..."` dans un dossier externe monté en volume.

## 📦 Prérequis
- Python 3.11+
- Un script `exporter.py` accessible (voir `SCRIPT_PATH` et `SCRIPT_DIRECTORY`).
- Un token Discord (voir `.env.example`).

## 🛠️ Installation (dev)
```bash
make init
cp .env.example .env  # remplis DISCORD_TOKEN & chemins exporter
make run
````

## 🧪 Tests & Qualité

```bash
make lint
make test
```

## 🐳 Docker

```bash
make docker-build
make docker-run
```

Monter le dossier contenant `exporter.py` sur `/app/external` (voir `.env`).

## 🔐 Variables d’environnement

* `DISCORD_TOKEN` : token du bot
* `SCRIPT_PATH` : chemin absolu vers `exporter.py` (dans le conteneur)
* `SCRIPT_DIRECTORY` : dossier de travail pour le script
* `LOG_LEVEL` : niveau de logs (INFO par défaut)
* `DATABASE_URL` : optionnel, `sqlite:///./data/questgen.db`
* `GUILD_IDS` : optionnel, ids de serveurs pour sync ciblée

## 🗄️ Base de données (optionnel)

Si `DATABASE_URL` est défini (SQLite supporté), un schéma minimal est créé pour historiser les générations de quêtes (voir `src/quest_generator_bot/db/init_db.py`).

## 🚦 CI/CD

* **CI** : lint + tests sur chaque PR/push `main`.
* **CD** : build & push image Docker sur tag `vX.Y.Z`. Exemple de déploiement SSH inclus (désactivé par défaut).

## 🧩 Arborescence

Voir le document de packaging dans ce repo.

## 🐞 Dépannage

* "DISCORD\_TOKEN manquant" → vérifier `.env`.
* Le script externe ne s’exécute pas → vérifier `SCRIPT_PATH`/`SCRIPT_DIRECTORY` et les volumes Docker.
* Slash commands non visibles → assure-toi d’avoir invité le bot avec les scopes/permissions et synchronisé sur les bons `GUILD_IDS`.

