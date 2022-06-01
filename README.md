# ocrp9
OpenClassRooms Projet 9  
Développez une application Web en utilisant Django

![Logo LITReview](https://raw.githubusercontent.com/FLinguenheld/ocrp9/main/logos/LITReview.png "Logo")
![Logo FLinguenheld](https://raw.githubusercontent.com/FLinguenheld/ocrp9/main/logos/forelif.png "Pouet")


****
### Description

L'objectif de ce projet est de découvrir le framework Django en réalisant le MVP d'une application web.  
Cette application doit permettre à une communauté d'utilisateurs de consulter et de demander des critiques d'œuvres (livres, articles…).   
Les utilisateurs peuvent :  
- Créer un compte et s'y connecter
- Créer des demandes de critique
- Répondre à une demande avec une critique
- Suivre d'autres utilisateurs


****
### Installation

Rendez-vous dans le dossier de votre choix puis lancez un terminal.  
Clônez le dossier depuis GitHub avec la commande :

    git clone https://github.com/FLinguenheld/ocrp9

Rendez-vous dans le dossier *ocrp9* et créez un nouvel environnement virtuel avec la commande :

    python -m venv env

Activez-le :

    source env/bin/activate

Les paquets nécessaires sont listés dans le fichier *requirement.txt*.  
Installez-les avec la commande :

    pip install -r requirement.txt


****
### Lancement

Rendez-vous dans le dossier *ocrp9* et activez l'environnement virtuel.  
Lancez le serveur avec la commande :  

    python manage.py runserver

*La console affichera les différentes requêtes effectuées. Vous pouvez arrêter le serveur en cliquant sur **Ctr-C***

Ouvrez votre navigateur web et entrez l'adresse suivante pour afficher l'application :

    http://localhost:8000/

****
### Tests

Afin de pouvoir tester l'application en local, le fichier SQLite est présent dans le dépôt GitHub.  
Il contient plusieurs utilisateurs :

```
Sophie14       PassDeTest14
Flo37          PassDeTest37
Henry62        PassDeTest62
admin          PassAdmin10
```

Pour accèder à la page d'administration, entrez l'adresse suivante puis connectez vous avec le compte *admin* :

    http://localhost:8000/admin/
