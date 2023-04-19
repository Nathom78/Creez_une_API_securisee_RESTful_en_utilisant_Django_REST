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

`PS D:\..\Developpez_une_application_Web_en-utilisant-Django> python -m venv .env`

Ensuite activer l'environnement python: 

`PS D:\..\Developpez_une_application_Web_en-utilisant-Django> .env\Scripts\activate.ps1`


## 3. Installer les paquets nécessaires aux projets.

<br>
Taper la commande suivante : 
<pre><code>
pip install -r requirements.txt
</code></pre>

Pour vérifier, taper cette commande :
<pre><code>pip list</code></pre>
Et vous devriez avoir :
<pre><code>Package           Version
----------------- -------
asgiref           3.6.0
Django            4.1.7
django-bootstrap5 22.2
Pillow            9.4.0
pip               23.0
setuptools        67.1.0
sqlparse          0.4.3
tzdata            2022.7
wheel             0.38.4
</code></pre>

## 4. Execution du logiciel

Dans une fenêtre de terminal, se placer à la racine de l'application
ici LITReview, ensuite taper les commandes suivantes :

Tout d'abord, nous devons appliquer les migrations à la base de donnée,
afin de pouvoir l'utiliser dans ce nouveau environnement la base db.sqlite.3 importer. 
<pre><code>
(.env) PS Developpez_une_application_Web_en-utilisant-Django\LITReview> py manage.py migrate
</code></pre>

Ensuite, nous pouvons lancer l'application à travers le serveur Django.

<pre><code>
(.env) PS Developpez_une_application_Web_en-utilisant-Django\LITReview> py manage.py runserver 
</code></pre>

Pour se connecter :

Superuser : (rôle : Administrateur) Thom / Thomas78190

Users : (rôle :utilisateur) Password: Thomas78190,
- Kathy
- Thomtest
- Toto
- Titi

ou créer un nouveau membre, là plus facilement grâce à l'application, onglet  **_"s'inscrire"_**

## Technologies
[![My Skills](https://skillicons.dev/icons?i=git,github,python,django&theme=dark)](https://skillicons.dev)
