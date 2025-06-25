# TP Final Test Methodo
##### Groupe Antoine DUCOUDRE et Vincent PARRA

Ce projet consiste à développer une API REST complète qui récupère des données météorologique d'une source. L'objectif est d'appliquer les bonnes pratiques de développement, notamment le Test-Driven Development (TDD), les tests de contrat, les tests de charge, et la mise en place d'un système de monitoring.

### Objectifs pédagogiques
- Maîtriser le développement d'API REST avec une approche TDD
- Implémenter des tests de différents niveaux (unitaires, intégration, contrat, charge)
- Mettre en place un système de monitoring et d'alertes
- Gérer la qualité du code et les métriques de performance

### Stack technologique recommandée
- **Backend** : Python avec FastAPI
- **Base de données** : PostgreSQL pour les données persistantes, Redis pour le cache
- **Tests** : pytest (Python)
- **Tests de charge** : Locust
- **Monitoring** : Prometheus + Grafana
- **Documentation** : Swagger
- **Docker** : Dockerisation

### Sources de données météo suggérées
**Open-Meteo** - [https://open-meteo.com/](https://open-meteo.com/)

### Requirements
Pour ce projet, plusieurs choses sont requises pour son bon fonctionnement.
- Vous devez avoir le daemon de Docker de lancé.
- Posséder un environnement virtuel python (via python ou uv)

Pour vérifier si votre daemon Docker est lancé :
Sur Linux :
```cmd
sudo status docker
```

Sur Windows :
```cmd
docker --version
```

Sur MacOS :
```cmd
docker info
```

Pour créer un environnement virtuel python :
Avec python :
```cmd
python3 -m venv .venv
```
Avec uv :
```cmd
uv init
```
ou
```cmd
uv venv
```
Activer votre venv et installer ensuite les packages nécessaires :
```cmd
pip install -r requirements.txt
```
```cmd
uv pip install -r requirements.txt
```
