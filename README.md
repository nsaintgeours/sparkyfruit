# Sparky'Fruit

Ce projet est un exemple minimaliste d'utilisation de Spark avec Python.
L'objectif est de traiter un grand nombre d'images disponibles sur un stockage AWS S3.
Le traitement consiste à encoder les images sous forme d'un vecteur de taille fixe à l'aide d'un réseau de neurones pré-entraîné.

## Création d'un espace de stockage S3 sur AWS

J'ai copié le jeu de données **Fruits 360 Dataset** sur un espace de stockage S3 lié à mon compte AWS :

- création d'un bucket via la console AWS en ligne
- création d'un utilisateur S3 via la console AWS en ligne
- enregistrement sur mon PC d'un fichier contenant les clés d'accès à mon stockage S3 : voir fichier `~/.aws/credentials`

## Fonctionnement en local (sur mon PC)

### Installation d'une machine virtuelle Linux sur mon poste

Spark ne fonctionne pas sous Windows. J'ai donc du installer une machine virtuelle Linux pour faire fonctionner le projet sur mon PC.

- téléchargement et installation de **Oracle VM VirtualBox**
- création d'une machine virtuelle Ubuntu, avec un espace disque de 100 Go
- configuration d'un dossier partagé entre mon PC et la machine virtuelle Ubuntu : partager le dossier contenant le code source de ce projet
- téléchargement de Apache Spark sur la machine virtuelle: `https://spark.apache.org/downloads.html`
- installation de pip pour python 3 sur la machine virtuelle
- installation des librairies python nécessaires au projet sur la machine virtuelle : voir fichier `requirements.txt`
- installation d'une librairie Java nécessaire pour accéder au stockage AWS S3 via Spark / Hadoop :

```
> sudo apt install openjdk-11-jdk
```

Le dernier point n'est nécessaire que pour le script `run_from_df.py`, pas pour le script `run_from_keys.py` qui lui accède
aux données stockées sur S3 en utilisation la librairie Python `boto3`.

On suppose qu'à la fin de cette installation :
- un dossier partagé nommé `sparkyfruit` est accessible depuis la machine virtuelle, il contient le code source de ce projet
- Spark est disponible à la racine de mon répertoire personnel : `~/spark-3.2.0-bin-hadoop3.2/`

### Configuration de Spark en local

Il faut éditer la configuration de Spark pour :
- réduire le niveau de log
- permettre l'accès aux données stockées sur AWS S3 directement via Spark / Hadoop

Note: le second point n'est nécessaire que pour le script `run_from_image_df.py`. Il n'est pas nécessaire pour le script
`run_from_image_keys.py` car celui-ci utilise la librairie Python `boto3` pour accèder aux données sur AWS S3.

Pour ce faire, on se rend dans le dossier `~/spark/conf` sur la machine virtuelle Ubuntu.

- copier le fichier `log4j.properties.template` vers un nouveau fichier `log4j.properties`
- copier le fichier `spark-defaults.conf.template` vers un nouveau fichier `spark-defaults.conf`
- éditer le fichier `spark-defaults.conf` en y ajoutant les lignes suivantes (les clés AWS S3 sont disponibles sur ma console AWS en ligne) :

```
spark.jars.packages             com.amazonaws:aws-java-sdk-bundle:1.11.901,org.apache.hadoop:hadoop-aws:-3.3.1
spark.hadoop.fs.s3a.access.key  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
spark.hadoop.fs.s3a.secret.key  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
spark.hadoop.fs.s3a.endpoint    s3.eu-west-3.amazonaws.com
spark.hadoop.fs.s3a.impl        org.apache.hadoop.fs.s3a.S3AFileSystem
```

Note: ces ajouts ne sont nécessaires que pour le script `run_from_image_df.py`. Il ne sont pas nécessaires pour le script
`run_from_image_keys.py` car celui-ci utilise la librairie Python `boto3` pour accèder aux données sur AWS S3.


- éditer le fichier `log4j.properties` en y modifiant la ligne suivante :

```
log4j.rootCategory=ERROR, console
```

### Lancer le job Spark en local

Le script doit être lancé sur la machine virtuelle Ubuntu. On suppose donc que celle-ci est ouverte et opérationnelle.
On commence par se déplacer dans le dossier partagé, contenant le script Python que l'on veut lancer : `run_from_image_df.py`.
On lance ensuite un job Spark avec comme argument notre script Python :

```
> cd ~/../../media/sf_sparkyfruit/src/
> ~/spark-3.2.0-bin-hadoop3.2/bin/spark-submit run_from_image_df.py
```

Pour surveiller l'exécution du job, il faut lancer un navigateur web et aller sur l'URL `localhost:4040` pour ouvrir
l'interface web de monitoring de Spark.

### Lancer le job Spark sur un cluster EC2

**A COMPLETER**
