# Projet8-Plateforme-de-substitution
### Création d'une plateforme de substitution d'aliments

Ce projet a pour but de créer une plateforme de substitution, sur laquelle un utilisateur pourra chercher un produit
et le substituer avec un autre plus sain. Cette plateforme est la suivante : **Pur Beurre**.
L'application a été déployée sur une instance AWS EC2.
**http://188.166.156.145**

Cette application a été developper avec **Django 3.0.4** et fait appel à **l'api d'OpenFoodFacts**

## Prérequis
- **Python** 3.7.7 ou supérieur.
- **Django** 3.0.4 ou supérieur.
- Les dépendances néccessaire à la bonne exécution de l'application se trouve dans le fichier requirements.txt

## Instalation local
Vous pouvez télécharger le repo pour avoir les fichiers néccessaires. Après avoir installé python, dans terminal :
```
cd dossier_du_programme
virutalenv nom_votre_environnment_virtuel
env/Scripts/Activate
pip install -r requirements.txt
```
Avant toute bonne éxecution de votre programme vous devez définir deux variables d'environnement : *SUB_PROJECT_SK* et *DEBUG_ENV_VARIABLE*.
Il existe deux façcon de faire ceci :
- Soit en les créant vous même sur votre systeme.
- Soit en changeant les variables *SECRET_KEY* et *DEBUG* dans le fichier **sub_project/settings.py**

### Population de la base de donnée
Pour que l'application fonctionne il faut remplir la base de données, cela ce fait avec la commande suivante (environnment virtuel activée):
```
python manage.py populate_database
```
