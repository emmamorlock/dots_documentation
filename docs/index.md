!!!! MAPPING RELATIVE PATHS!

Multiple collections => seulement 2!

- Pas listé sur la coll racine
- Les membres ne sont pas listés
- PB avec data/ path ????

Que se passe si pas de sous-dossiers in data/ ?

# Installer DoTS

**1. BaseX**

Télécharger BaseX (>= 10.0): [https://basex.org/download/](https://basex.org/download/)

- Privilégier le `ZIP Package`
- Pré-requis : [https://docs.basex.org/wiki/Startup#Startup](https://docs.basex.org/wiki/Startup#Startup)


**2. DoTS**


Exécuter les commandes :

```bash
cd path/to/basex/webapp
git clone https://github.com/chartes/dots.git
```

La structure de votre instance BaseX doit être la suivante :


	basex/			# BaseX root dir
		bin/		# Start scripts (GUI, HTTP server, etc.)
		data/		# The database directory
		webapp/		# Web Application directory
			dots/	# DoTS module (DTS reslover, etc.)
		...			# Other



La structure de `webapp/dots` est la suivante :

	dots/
		api/
		lib/				# anciennement builder et db : les modules xqm
		scripts/			# anciennement manage : des utilitaires



# Préparer un dossier de dépôt

Pour publier un projet, il vous reste à préparer son dossier de dépôt qui sera chargé en base grâce aux outils DoTS.

Un peu de vocabulaire.

## Vocabulaire

**Projet**. Un "projet" est une collection DTS de premier niveau, un corpus éditorial défini. Par exemple, il est possible de donner accès via un même endpoint DTS à des correspondances ET à des pièces de théâtre : on distinguera donc le projet *Correspondance* et le projet *Théâtre*.


**Dossier de dépôt**. Pour être correctement chargé en base avec les outils DoTS, un projet doit être structuré dans un dossier conformément aux attendus de DoTS. Ce dossier est désigné dans la documentation par l’expression "dossier de dépôt".

**Base de données projet** ou **DB projet**. Chaque projet (chaque collection de premier niveau) est importé sous la forme d’une base de données BaseX. Les projets *Correspondance* et *Théâtre* sont chargés sous la forme de 2 bases de données distinctes, par exemple respectivement `correspondance` et `theatre`.

## Workflow

TODO Diagramme

```
project_working_dir/
	|
	---scripts maison----->dossier de dépôt
									|
									------>dots
												|
												----->db projet
```

NB. Idéalement le dossier de dépôt est le dossier de travail.


## Structuration du dossier de dépôt

	nom_projet/							# racine du dossier de dépôt
		data/							# OBLIGATOIRE. les fichiers TEI en dossiers de collection
			collection_1/				# collection 1
				file_1.xml
				file_2.xml
				…
			collection_2/				# collection 2
				file_100.xml
				file_101.xml
				…
		metadata/						# OPTIONNEL. les métadonnées des collections et des documents
			dots_metadata_mapping.xml	# déclaration du chemin des métadonnées
			metadata_1.tsv				# un fichier de métadonnées
			metadata_2.tsv				# un fichier de métadonnées
			…


- Racine du projet – `nom_projet/`. Le nom de ce dossier est libre. Au chargement en base, vous pourrez spécifier le nom de la base de données BaseX, l’identifiant DTS attribué à la collection racine ainsi que lui attribuer un titre.

- Les documents XML/TEI – `data/`. Ce dossier est **obligatoire**. Il contient les sources XML/TEI de votre projet organisées selon la hiérarchie de votre choix. Cette hiérarchie représente les collections par défaut de votre projet. Par exemple, ici, les documents `file_1.xml` et `file_2.xml` appartiennent à la collection `collection_1`.

- Les métadonnées – `metadata/`. Ce dossier est **optionnel**. TODO

- `tei:citeStructure`. TODO documenter l’usage de cet élément pour la définition des fragments


## Exemples

La structuration du *dossier de dépôt* reflète la structure éditoriale du projet.

TODO: développer

**Liens au cookbook :**

- [périodiques](cookbook/#publier-un-periodique)
- cartulaire / registre
- théâtre
- correspondance
- roman
- poésie
- dictionnaire


# Chargement (dots) d’un projet

## Initialisation de la DB dots


```bash
cd path/to/basex/bin
bash basex ../webapp/dots/scripts/dots_db_init.xq
```

TODO Doc

## Création de la base de données projet


```bash
cd path/to/basex/bin
bash basex -b dbName=db_name -b projectDirPath=/path/to/dossier/de/depot ../webapp/dots/scripts/project_db_init.xq
```

On doit spécifier les arguments suivants :

- `dbName` : nom de la base de données BaseX du projet
- `projectDirPath` : chemin absolu vers le dossier de dépôt du projet

La base de données du projet est créée en conservant la structure du paquet de dépôt en collections et sous-collection par défaut. Mais il est d’inscrire ces documents dans d’autres collections.


## Création des registres du projet


```bash
bash basex -b dbName=db_name -b topCollectionId=top_collection_id ../webapp/dots/scripts/project_registers_create.xq
```

On doit spécifier les arguments suivants :

- `dbName` : nom de la base de données BaseX du projet
- `topCollectionId` : identifiant DTS de la collection racine du projet

**NB. La base de données du projet ne DOIT PAS être ouverte dans le GUI BaseX**.


## Mise à jour du switcher DoTS

Le switcher de la base de données DoTS (`dots_db_switcher.xml`) sert à associer les identifiants des ressources (collections et documents) à leur base de données de projet d’appartenance.


```bash
bash basex -b dbName=db_name ../webapp/dots/scripts/dots_switcher_update.xq
```

On doit spécifier l’argument suivant :

- `dbName` : nom de la base de données BaseX du projet à parcourir pour mise à jour du switcher. Ainsi, on peut mettre à jour la base pour un unique projet.


Et voilà. Les ressources de votre projet sont décrites et accessibles via les endpoints DTS fournis par DoTS.


## Créer de nouvelles collections et y attacher des documents (existants)


```bash
bash basex -b srcPath=/path/to/custom_collections.tsv ../webapp/dots/scripts/create_custom_collections.xq 
```

TODO documentation de `custom_collections.tsv`



## Supprimer les registres DoTS d’un projet

Le script `dots_registers_delete.xq` supprime les registres DoTS d’un projet. Dans le même temps, il supprime toutes les entrées correspondant à ce projet dans le switcher DoTS. TODO réécrire.

```bash
bash basex -b dbName=db_name ../webapp/dots/scripts/dots_registers_delete.xq
```

On doit spécifier l’argument suivant :

- `dbName` : nom de la base de données BaseX du projet à parcourir suppression des registres DoTS.
