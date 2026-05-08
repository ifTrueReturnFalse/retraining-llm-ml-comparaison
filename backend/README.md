# Backend et analyse des données du projet

Dans ce dossier ce trouve le nécessaire pour gérer le backend du projet ainsi que l'analyse des données.

## Commandes

### Frontend

> [!important]
> Ces commandes sont à lancer dans le dossier `frontend`

```bash
# Démarrer le serveur web
npm run dev

# Démarrer la base de données (avec Docker)
npm run db:start

# Reset la BDD (avec Docker)
npm run db:reset

# Arrêter la BDD (avec Docker)
npm run db:stop
```

### Backend

> [!important]
> Ces commandes sont à lancer dans le dossier `backend`

```bash
# Converti le fichier au format csv vers le feather 
uv run convert

# Fais un échantillonage stratifié du dataset
uv run sample

# Entraine un modèle de classification et l'export vers le format pickle (librairie joblib pour la création / export)
uv run train_export

# Démarre l'API du backend pour exposer le modèle de classification
uv run api
```