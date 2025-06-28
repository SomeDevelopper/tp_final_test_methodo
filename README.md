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
- **Tests** : pytest (Python) + schemathesis
- **Tests de charge** : Locust
- **Monitoring** : Prometheus + Grafana + Loki
- **Documentation** : Swagger
- **Docker** : Dockerisation

### Sources de données météo suggérées
**Open-Meteo** - [https://open-meteo.com/](https://open-meteo.com/)

### Requirements
Pour ce projet, plusieurs choses sont requises pour son bon fonctionnement.
- Vous devez avoir le daemon de Docker de lancé.
- Posséder un environnement virtuel python (via python ou uv) avec une version 3.11

Si vous devez installer les différents services, vous pouvez vous référez à ces différentes documentations : 
- https://www.python.org/downloads/
- https://docs.docker.com/engine/install/
- https://docs.astral.sh/uv/getting-started/installation/

Pour vérifier si votre daemon Docker est lancé :
Sur **Linux** :
```cmd
sudo status docker
```

Sur **Windows** :
```cmd
docker --version
```

Sur **MacOS** :
```cmd
docker info
```

Pour créer un environnement virtuel python :
Avec **python** :
```cmd
python3 -m venv .venv
```
Avec **uv** :
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

### Variables d'environnement
Un fichier **.env** est requis pour le fonctionnement du projet. Si aucun fichier n'est mit à la racine du projet, celui-ci utilisera les variables de configuration prédéfinits.
Un fichier **.env.example** est renseigné pour vous aidez sur la structure.
Une fois le fichier **.env** créer, pensez à supprimer le fichier **.env.example**

### Lancement des services
Avant de lancé le serveur API, vous devez monter les images et créez les containers des différents services avec docker.
Pour cela, exécutez la commande suivante :
```cmd
docker compose up --build -d
```

#### Serveur API
Une fois tous les containers créés, vous pouvez maintenant lancer le serveur Fast API.

Pour cela exécuté la commande suivant : 
- Avec l'**environnement python**
```cmd
python app.py
```
- Avec l'**environnement uv** 
```cmd
uv run app.py
```

Une fois le serveur lancé, vous pouvez maintenant accéder à la documentation swagger des routes de l'API via l'url suivant : 
http://localhost:3000/docs

!!!Warning Pensez à bien le laisser tourné durant tout le processus, pour les tests ainsi que le monitoring

Dans cette documentation, vous pourrez retrouver et vous pourrez tester 4 routes :
- `GET /weather/current/:city` - Météo actuelle (qui prend en paramètre une ville)
- `GET /weather/forecast/:city` - Prévisions sur 5 jours (qui prend en paramètre une ville)
- `GET /weather/history/:city` - Données historiques (qui prend en paramètre une ville)
- `GET /health` - Vérification de l'état de l'API

#### Service Monitoring
Si vous avez bien créer vos containers docker, les services de monitoring (Grafana, Loki et Prometheus) sont créés et en train de tourner. 
Vous pouvez vérifier cela ainsi que leurs ports en exécutant la commande suivante :
```cmd
docker ps
```
Une fois cela vérifié, vous pouvez accéder à Grafana, le service de monitoring directement via le lien : 
http://localhost:3001
Pour vous connectez, les crédentials sont les suivants : 
**username** : admin
**password** : admin
Une fois connecté pour la première fois, ous serez amenez à modifier le mot de passe de l'administrateur.

Vous y retrouver le nombre de requêtes effectuées pour les différentes routes avec un code 200 et le nombre de requêtes pour chaque routes avec un code différent de 200.

### Lancement des Tests
Pour ce projet, différents tests ont été mit en place, des tests TDD, tests de contrats et stressing test.
#### Tests Unitaires
Ces tests nous permettent de tester les fonctionnalités du code sources et ainsi valider leurs bon fonctionnements. Le but étant de courvir l'ensemble du code source.
Pour éxécuter les tests unitaires, on peut exécuter la commande : 
```cmd
coverage run -m pytest && coverage report -m
```
!!!Attention Avant d'exécuter les tests, vous devez avoir votre docker daemon qui tourne en arrière-plan, il est nécessaire pour leur bon fonctionnement.

A la suite des tests, plusieurs informations seront données : 
- quels tests sont passés ou non
- un tableau coverage pour savoir la couverture de code des tests

#### Tests de contrats
Les tests de contrats (ou contract tests) servent à garantir que deux systèmes communiquent correctement entre eux, selon un contrat défini.
Pour effectuer les tests de contrats, vous devez d'abord lancer le serveur API puis ensuite effectuer cette commande : 
```cmd
schemathesis run http://127.0.0.1:3000/openapi.json
```
Elle ressortir un résumé des différents tests de contrats effectués.

#### Stressing Tests
Les stressing tests nous permettent de tester les performances de l'applications en effectuant plusieurs requêtes simultanées sur le serveur.
Pour effectué ces tests, lancer le serveur API ainsi que les serveurs locust via la commande : 
```cmd
locust -f src/tests/locustfile.py --host=http://127.0.0.1:3000
```
Une fois le serveur lancé, vous pouvez accéder à l'interface locust via le lien : 
http://localhost:8089
Vous pouvez ensuite configurer un nombre d'utilisateur pour le tests et les lancez.
Vous aurez durant et à la fin du test, vous aurez une vue sur différente information comme le temps de réponse, la route utilisée.

!!!Attention Pensez bien à lancer le serveur API avant d'effectuer les tests