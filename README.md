# Créez une API sécurisée RESTful en utilisant Django REST
[Projet 10 du parcours OpenClassrooms Développeur d'application - Python](https://openclassrooms.com/fr/paths/518/projects/838/assignment)

### Prérequis
* Python est bien installé sur votre ordinateur
* Git installé (conseillé)

# INSTALLATION ( pour windows )

Créer un dossier vide. Il contiendra le code complet du projet
## 1. Installation du site

Ouvrez un terminal:

Depuis le dossier précédemment créé, clonez le repository du programme avec la commande :

<pre><code>git clone https://github.com/Nathom78/Creez_une_API_securisee_RESTful_en_utilisant_Django_REST.git</code></pre>

Ou utiliser [ce repository](https://github.com/Nathom78/Creez_une_API_securisee_RESTful_en_utilisant_Django_REST.git) en téléchargeant le zip.
<br>


## 2. Installer un environnement python

D'abord créer à partir de la racine du projet un environnement, ici appellé ".env"

`PS D:\..\Creez_une_API_securisee_RESTful_en_utilisant_Django_REST> python -m venv .env`

Ensuite activer l'environnement python: 

`PS D:\..\Creez_une_API_securisee_RESTful_en_utilisant_Django_REST> .env\Scripts\activate.ps1`


## 3. Installer les paquets nécessaires aux projets.

<br>
Taper la commande suivante : 
<pre><code>
pip install -r requirements.txt
</code></pre>

Pour vérifier, taper cette commande :
<pre><code>pip list</code></pre>
Et vous devriez avoir :
<pre><code>Package             Version
------------------- ---------
asgiref             3.6.0
certifi             2022.12.7
charset-normalizer  3.1.0
coreapi             2.3.3
coreschema          0.0.4
Django              4.2.1
djangorestframework 3.14.0
drf-yasg            1.21.5
idna                3.4
inflection          0.5.1
itypes              1.2.0
Jinja2              3.1.2
MarkupSafe          2.1.2
packaging           23.1
pip                 23.1.2
pytz                2023.3
requests            2.28.2
ruamel.yaml         0.17.21
setuptools          67.7.0
sqlparse            0.4.4
tzdata              2023.3
uritemplate         4.1.1
urllib3             1.26.15
</code></pre>

## 4. Execution du logiciel

Dans une fenêtre de terminal, se placer à la racine de l'application
ici SoftDesk, ensuite taper les commandes suivantes :

Tout d'abord, nous devons appliquer les migrations à la base de donnée,
afin de pouvoir utiliser dans ce nouvel environnement, la base db.sqlite3 importée. 
<pre><code>
(.env) PS ~...\SoftDesk> py manage.py migrate
</code></pre>

Ensuite, nous pouvons lancer l'application à travers le serveur Django.

<pre><code>
(.env) PS ~...\SoftDesk> py manage.py runserver 
</code></pre>



## Technologies
[![My Skills](https://skillicons.dev/icons?i=git,github,python,django,postman&theme=dark)](https://skillicons.dev)

## Administrateur Django:
Admin / 
Admin