# Sparky'Fruit (AWS, AMI Amazon Linux 2)

Ce projet est un exemple minimaliste d'utilisation de Spark avec Python.
L'objectif est de traiter un grand nombre d'images disponibles sur un stockage AWS S3.
Le traitement consiste à encoder les images sous forme d'un vecteur de taille fixe à l'aide d'un réseau de neurones pré-entraîné.

## 0. Création d'un compte AWS

- Depuis un navigateur web : 
	- Créer un compte AWS
	- Se connecter à son compte AWS
	- Accéder à la 'AWS Management Console' (https://eu-west-3.console.aws.amazon.com/console)

## 1. Stocker un échantillon de données sur AWS S3

- Dans la 'AWS Management Console'  en ligne :

	- Accéder au service S3 : https://s3.console.aws.amazon.com/s3
	
	- Créer un bucket S3 avec la configuration suivante : 
		- bucket name: sparkyfruit 
		- AWS region: EU (Paris) eu-west-3
		- Object ownership: ACLs disabled
		- Block all public access
		- Bucket versioning: Disable
		- No tags
		- Server-side encryption: Disable
		
	- Uploader à la main un échantillon de photos de fruits dans le bucket S3 :
	    - Créer un dossier différent pour chaque classe de fruit (2 ou 3 classes)
		- Dans chaque dossier, uploader une dizaine de photos de fruits


## 2. Créer un serveur virtuel dans le cloud (EC2)

- Dans la 'AWS Management Console'  en ligne :

	- Accèder au service EC2 : https://eu-west-3.console.aws.amazon.com/ec2
	
	- Menu de gauche : sélectionner "Instances"
	
	- Bouton orange en haut à droite : Launch instances / Launch instances
	
	- Lancer une instance EC2 avec les caractéristiques suivantes : 
	
		- name: sparkyfruit
		- Amazon Machine Image (AMI): laisser le choix par défaut ("Amazon Linux 2 AMI (HVP) - Kernel 5.10 SSD volume type"), 64 bits
		- Instance type : t2.medium (4 GO RAM, 30 Go disque dur) (coût estimé < 10 Euros) 
		- Key pair (login) : cliquer sur "Generate a new key pair" et se laisser guider (sélectionner "Proceed without a key pair (Not recommended)")
		- Network settings : 
			- Firewall (security groups) : sélectionner "Create security group" avec la configuration suivante :
				- Allow SSH traffic from : Anywhere
				- Allow HTTPs traffic from the internet: No
				- Allow HTTP traffic from the internet: No
		- Configure storage : 1 x 30 GiB gp2 (root volume)
		- Lancer l'instance (ça peut prendre une ou deux minutes)
		
		
	- On va maintenant ajouter une autorisation d'accès au serveur virtuel pour pouvoir accéder aux notebooks Jupyter par la suite : 
		- Menu de gauche, aller dans Network & Security / Security Groups
		- Sélectionner dans la liste le groupe de sécurité qui vient d'être créé, il s'appelle "launch-wizard-1" (case à cocher à gauche)
		- En bas on voit les propriétés du groupe de sécurité : sélectionner l'onglet "Inbound rules"
		- Bouton "Edit inbound rules"
		- Bouton "Add rule" : ajouter une règle d'accès avec les caractéristiques suivantes : 
			- Tpe : Custom TCP
			- Protocol : TCP
			- Port range: 8888
			- Source: Anywhere ipv4
		- Cliquer sur le bouton "Save rules"
		
		
	- On peut maintenant se connecter à l'instance EC2 : 
		- Menu de gauche : sélectionner "Instances"
		- Dans la liste des instances, sélectionner l'instance que l'on vient de démarrer (case à cocher à gauche du nom de l'instance)
		- Bouton "Connect" -> on arrive sur un menu "Connect to instance", laisser les options par défaut et cliquer en bas sur le bouton orange "Connect"
		- une nouvelle page s'ouvre dans le navigateur web, avec une console Linux


## 3. Accèder à un notebook Jupyter dans le cloud (EC2)

- Depuis Ia console Linux ouverte au point précedent, installer les outils suivants sur l'instance EC2 : 

	- Python3 est déjà installé par défaut, on peut vérifier la version avec :
	
	```
	[ec2-user@ip-172-31-33-35 ~]$ python3 --version
	Python 3.7.10
	```
	
	- installer Jupyter (à l'aide de pip3, gestionnaire de packages Python): 
	
	```
	[ec2-user@ip-172-31-33-35 ~]$ pip3 install jupyter
	```
	
	- on configure un nouveau mot de passe pour sécuriser l'accès aux notebooks Jupyter dans le cloud 
	
	```
	[ec2-user@ip-172-31-33-35 ~]$ jupyter notebook password
	```
	
	- on lance Jupyter Notebook (avec des options utiles pour que ça fonctionne sur l'instance EC2) : 

	```
	[ec2-user@ip-172-31-33-35 ~]$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
	```

- Dans le navigateur web, revenir sur le service EC2 : https://eu-west-3.console.aws.amazon.com/ec2

	- Menu de gauche, aller dans Instances / Instances
		- Dans la liste des instances EC2, sélectionner l'instance EC2 que l'on a démarré (case à cocher à gauche)
		- En bas, dans les propriétés de l'instance, noter la "Public IPv4 address" (ex: 13.39.47.167). 
			(attention : cette adresse publique de notre instance EC2 change à chaque arrêt redémarrage de l'instance !)
		
	- Dans le navigateur web, accèder à l'URL suivante : xx.xx.xx.xxx:8888, en remplaçant xx.xx.xx.xxx par l'adresse IP publique de l'instance EC2
	
	- Le serveur Jupyter Notebook s'ouvre, avec sécurisation de l'accès par le mot de passe que l'on a défini précédemment
	
	- Créer un nouveau notebook, l'ouvrir, et tester si tout fonctionne !


## 4. Accèder aux images stockées sur S3 depuis le notebook Jupyter

- On commence par donner à notre instance EC2 les droits d'accès à l'espace de stokage S3 : 

	- Dans un navigateur web, ouvrir la "AWS Management Console" et accèder au service **IAM**
		- Menu de gauche : Roles
		- Bouton Create Roles	
			- Trusted Entity Type : laisser par défaut la valeur "AWS Service"
			- Use case : sélectionner "EC2"
		- Permission policies : rechercher **AmazonS3FullAccess**
		- Bouton "Create Role"
		
	- Dans un navigateur web, ouvrir la "AWS Management Console" et accèder au service EC2	
		- Menu de gauche, Instances / Instances
		- Sélectionner notre instance (case à cocher à gauche)
		- En haut, menu Actions / Security / Modify IAM role
		- Sélectionner le role que l'on a créé, puis bouton "Update IAM Role"
		
	- Console Linux EC2 : 
	
	```
	[ec2-user@ip-172-31-33-35 ~]$ aws s3 ls s3://sparkyfruit
	--> on doit avoir la liste des dossiers sdans le bucket s3
	```

- Depuis Ia console Linux ouverte au point 2, installer la librairie Python boto3, qui permet d'interagir avec l'espace de stockage AWS S3 :

	```
	[ec2-user@ip-172-31-33-35 ~]$ pip3 install boto3
	```
	
- Depuis Ia console Linux ouverte au point 2, installer la librairie Python pillow, qui permet de manipuler des images :

	```
	[ec2-user@ip-172-31-33-35 ~]$ pip3 install pillow
	```
	
- Relancer le serveur Jupyter Notebook et ouvrir un notebook ((voir point précédent)

- Dans le notebook Jupyter, le bloc de code suivant permet de charger et d'afficher une des images stockées sur votre bucket S3 : 

	```
	import boto3
	import PIL.Image

	s3_bucket_name = "sparkyfruit"
	image_key = "apple_6/r1_216.jpg"

	s3 = boto3.client('s3')
	image = s3.get_object(Bucket=s3_bucket_name, Key=image_key)
	PIL.Image.open(image['Body'])
	```



## 5. Installer Spark et PySpark

```
sudo amazon-linux-extras install java-openjdk11
```

```
pip3 install pyspark
```


# Sparky'Fruit (AWS, AMI Ubuntu)

Ce projet est un exemple minimaliste d'utilisation de Spark avec Python.
L'objectif est de traiter un grand nombre d'images disponibles sur un stockage AWS S3.
Le traitement consiste à encoder les images sous forme d'un vecteur de taille fixe à l'aide d'un réseau de neurones pré-entraîné.

## 0. Création d'un compte AWS

- Depuis un navigateur web : 
	- Créer un compte AWS
	- Se connecter à son compte AWS
	- Accéder à la 'AWS Management Console' (https://eu-west-3.console.aws.amazon.com/console)

## 1. Stocker un échantillon de données sur AWS S3

- Dans la 'AWS Management Console'  en ligne :

	- Accéder au service S3 : https://s3.console.aws.amazon.com/s3
	
	- Créer un bucket S3 avec la configuration suivante : 
		- bucket name: sparkyfruit 
		- AWS region: EU (Paris) eu-west-3
		- Object ownership: ACLs disabled
		- Block all public access
		- Bucket versioning: Disable
		- No tags
		- Server-side encryption: Disable
		
	- Uploader à la main un échantillon de photos de fruits dans le bucket S3 :
	    - Créer un dossier différent pour chaque classe de fruit (2 ou 3 classes)
		- Dans chaque dossier, uploader une dizaine de photos de fruits


## 2. Créer un serveur virtuel dans le cloud (EC2)

- Dans la 'AWS Management Console'  en ligne :

	- Accèder au service EC2 : https://eu-west-3.console.aws.amazon.com/ec2
	
	- Menu de gauche : sélectionner "Instances"
	
	- Bouton orange en haut à droite : Launch instances / Launch instances
	
	- Lancer une instance EC2 avec les caractéristiques suivantes : 
	
		- name: sparkyfruit
		- Amazon Machine Image (AMI): selectionner Ubuntu (Ubuntu Server 22.04 LTS (HVM), SSD Volume Type, 64 bits)
		- Instance type : t2.medium (4 GO RAM, 30 Go disque dur) (coût estimé < 10 Euros) 
		- Key pair (login) : cliquer sur "Generate a new key pair" et se laisser guider (sélectionner "Proceed without a key pair (Not recommended)")
		- Network settings : 
			- Firewall (security groups) : sélectionner "Create security group" avec la configuration suivante :
				- Allow SSH traffic from : Anywhere
				- Allow HTTPs traffic from the internet: No
				- Allow HTTP traffic from the internet: No
		- Configure storage : 1 x 30 GiB gp2 (root volume)
		- Lancer l'instance (ça peut prendre une ou deux minutes)
		
		
	- On va maintenant ajouter une autorisation d'accès au serveur virtuel pour pouvoir accéder aux notebooks Jupyter par la suite : 
		- Menu de gauche, aller dans Network & Security / Security Groups
		- Sélectionner dans la liste le groupe de sécurité qui vient d'être créé, il s'appelle "launch-wizard-1" (case à cocher à gauche)
		- En bas on voit les propriétés du groupe de sécurité : sélectionner l'onglet "Inbound rules"
		- Bouton "Edit inbound rules"
		- Bouton "Add rule" : ajouter une règle d'accès avec les caractéristiques suivantes : 
			- Tpe : Custom TCP
			- Protocol : TCP
			- Port range: 8888
			- Source: Anywhere ipv4
		- Cliquer sur le bouton "Save rules"
		
		
	- On peut maintenant se connecter à l'instance EC2 : 
		- Menu de gauche : sélectionner "Instances"
		- Dans la liste des instances, sélectionner l'instance que l'on vient de démarrer (case à cocher à gauche du nom de l'instance)
		- Bouton "Connect" -> on arrive sur un menu "Connect to instance", laisser les options par défaut et cliquer en bas sur le bouton orange "Connect"
		- une nouvelle page s'ouvre dans le navigateur web, avec une console Linux


## 3. Accèder à un notebook Jupyter dans le cloud (EC2)

- Depuis Ia console Linux ouverte au point précedent, installer les outils suivants sur l'instance EC2 : 

	- Python3 est déjà installé par défaut, on peut vérifier la version avec :
	
	```
	[ubuntu@ip-172-31-33-35 ~]$ python3 --version
	Python 3.10.4
	```
	
  
	- installer Jupyter (taper sur Entrée quand des fenêtre chelous s'affichent sur la console...)
	
	```
	[ubuntu@ip-172-31-33-35 ~]$ sudo apt install jupyter-notebook
	```
	
	- on configure un nouveau mot de passe pour sécuriser l'accès aux notebooks Jupyter dans le cloud 
	
	```
	[ubuntu@ip-172-31-33-35 ~]$ jupyter notebook password
	```
	
	- on lance Jupyter Notebook (avec des options utiles pour que ça fonctionne sur l'instance EC2) : 

	```
	[ubuntu@ip-172-31-33-35 ~]$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
	```

- Dans le navigateur web, revenir sur le service EC2 : https://eu-west-3.console.aws.amazon.com/ec2

	- Menu de gauche, aller dans Instances / Instances
		- Dans la liste des instances EC2, sélectionner l'instance EC2 que l'on a démarré (case à cocher à gauche)
		- En bas, dans les propriétés de l'instance, noter la "Public IPv4 address" (ex: 13.39.47.167). 
			(attention : cette adresse publique de notre instance EC2 change à chaque arrêt redémarrage de l'instance !)
		
	- Dans le navigateur web, accèder à l'URL suivante : xx.xx.xx.xxx:8888, en remplaçant xx.xx.xx.xxx par l'adresse IP publique de l'instance EC2
	
	- Le serveur Jupyter Notebook s'ouvre, avec sécurisation de l'accès par le mot de passe que l'on a défini précédemment
	
	- Créer un nouveau notebook, l'ouvrir, et tester si tout fonctionne !




## 4. Accèder aux images stockées sur S3 depuis le notebook Jupyter

- On commence par donner à notre instance EC2 les droits d'accès à l'espace de stokage S3 : 

	- Dans un navigateur web, ouvrir la "AWS Management Console" et accèder au service **IAM**
		- Menu de gauche : Roles
		- Bouton Create Roles	
			- Trusted Entity Type : laisser par défaut la valeur "AWS Service"
			- Use case : sélectionner "EC2"
		- Permission policies : rechercher **AmazonS3FullAccess**
		- Bouton "Create Role"
		
	- Dans un navigateur web, ouvrir la "AWS Management Console" et accèder au service EC2	
		- Menu de gauche, Instances / Instances
		- Sélectionner notre instance (case à cocher à gauche)
		- En haut, menu Actions / Security / Modify IAM role
		- Sélectionner le role que l'on a créé, puis bouton "Update IAM Role"
		

- Depuis Ia console Linux ouverte au point 2 : 

	- installer le gestionnaire de package Python pip3
	```
	[ubuntu@ip-172-31-33-35 ~]$ sudo apt-get update
	[ubuntu@ip-172-31-33-35 ~]$ sudo apt-get install python3-pip
	```

  - installer la librairie Python boto3, qui permet d'interagir avec l'espace de stockage AWS S3 :
	```
	[ubuntu@ip-172-31-33-35 ~]$ pip3 install boto3
	```
	
  - installer la librairie Python pillow, qui permet de manipuler des images :

	```
	[ubuntu@ip-172-31-33-35 ~]$ pip3 install pillow
	```
	
- Relancer le serveur Jupyter Notebook et ouvrir un notebook ((voir point précédent)

- Dans le notebook Jupyter, le bloc de code suivant permet de charger et d'afficher une des images stockées sur votre bucket S3 : 

	```
	import boto3
	import PIL.Image

	s3_bucket_name = "sparkyfruit"
	image_key = "apple_6/r1_216.jpg"

	s3 = boto3.client('s3')
	image = s3.get_object(Bucket=s3_bucket_name, Key=image_key)
	PIL.Image.open(image['Body'])
	```
  
## 5. Installer Spark et PySpark

```
sudo amazon-linux-extras install java-openjdk11
```

```
pip3 install pyspark
```


  
# Sparky'Fruit (local)

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
