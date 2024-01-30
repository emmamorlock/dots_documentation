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

- Les métadonnées – `metadata/`. Ce dossier est **optionnel**.

**TODO. Détailler**

- les contraintes
- optionnel/obligatoire
- méthodes pour le produire

## Exemples

la structuration reflète la structure éditoriale du projet.

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

TODO : création de la DB dots avec switcher vide et le data_mapping par défaut (à conserver ?)
	
Création de la base de données dots, avec 2 fichiers

- `dots_db_switcher.xml` : TODO documenter
- `dots_default_metadata_mapping.xml` : TODO documenter


## Création de la base de données projet


```bash
cd path/to/basex/bin
bash basex -b dbName=db_name -b projectDirPath=/path/to/dossier/de/depot ../webapp/dots/scripts/project_db_init.xq
```

MEMO EXEMPLE

```bash
cd path/to/basex/bin
bash basex -b dbName=encpos-c1 -b projectDirPath=/Users/bolsif/Documents/enc/corpus/dots_documentation/data_test/periodiques/encpos_by_abstract ../webapp/dots/scripts/project_db_init.xq
```


documenter les arguments :

- `dbName` : nom de la base de données BaseX du projet
- `projectDirPath` : chemin absolu vers le dossier de dépôt du projet

TODO : Annoncer la création de la DB du projet

NB. La db conserve la structure du paquet de dépôt (cf la hiérarchie), mais il reste possible de définir d’autres collections.



TODO rejeter au bon endroit ces tableaux de doc

| Variable | Description | Exemple | Type |
| -------- | -------- | -------- | -------- |
| `$topCollectionId`     | identifiant de la collection racine du projet     | `ENCPOS` | obligatoire     |
| `$dbName`     | nom de la base de données BaseX du projet     | `encpos` | obligatoire     |
| `$projectDirPath`   | chemin absolu vers le paquet de dépôt du projet (sources TEI, etc.)    | `/path/to/project/` | obligatoire     |

à évaluer : rejetter en globals ?

| Variable | Description | Exemple | Type |
| -------- | -------- | -------- | -------- |
| `$dbc:separator`      | déclaration du caractère séparateur dans le tableur CSV     | (*TAB*) | facultatif     |
| `$dbc:language`   | Langue de la db (pour indexation)     | *fr* | obligatoire     |




## Création des registres du projet


```bash
bash basex -b dbName=db_name -b topCollectionId=top_collection_id ../webapp/dots/scripts/project_registers_create.xq
```


```bash
bash basex -b dbName=encpos-c1 -b topCollectionId=ENCPOS ../webapp/dots/scripts/project_registers_create.xq
```

NB. La db ne DOIT PAS être ouverte dans le GUI.

- Utile de conserver en base les TSV et même le mapping ? => non mais on conserve dans metadata/


## Mise à jour de la db dots (le switcher)

TODO: voir si on peut lancer le script automatiquement après celui de création des registres du projet

```bash
bash basex -b dbName=db_name ../webapp/dots/scripts/dots_switcher_update.xq
```

Par exemple:

```bash
bash basex -b dbName=encpos-c1 ../webapp/dots/scripts/dots_switcher_update.xq
```


## Resolver

Lancer basexhttp: https://docs.basex.org/wiki/Web_Application

```sh
basex % bin/basexhttp
```

consulter [http://0.0.0.0:8080/api/dts/](http://0.0.0.0:8080/api/dts/)