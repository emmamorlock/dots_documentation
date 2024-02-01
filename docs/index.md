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
		lib/				
		schema/
		scripts/	
		globals.xqm
		README.md



# Préparer un dossier de dépôt

Pour publier un projet, il vous reste à préparer son dossier de dépôt qui sera chargé en base grâce aux outils DoTS.

Un peu de vocabulaire.

## Vocabulaire

**<a id="projet">Projet</a>**. Un "projet" est une collection DTS de premier niveau, un corpus éditorial défini. Par exemple, il est possible de donner accès via un même endpoint DTS à des correspondances ET à des pièces de théâtre : on distinguera donc le projet *Correspondance* et le projet *Théâtre*.


**Dossier de dépôt**. Pour être correctement chargé en base avec les outils DoTS, un *projet* doit être structuré dans un dossier conformément aux attendus de DoTS. Ce dossier est désigné dans la documentation par l’expression "dossier de dépôt".

**Base de données projet** ou **DB projet**. Chaque *projet* (chaque collection racine) est importé sous la forme d’une base de données BaseX. Les projets *Correspondance* et *Théâtre* sont chargés sous la forme de 2 bases de données distinctes, par exemple respectivement `correspondance` et `theatre`.

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


- Racine du projet – `nom_projet/`. Le nom de ce dossier est libre. Au chargement en base, vous pourrez spécifier le nom de la base de données BaseX, et l’identifiant DTS attribué à la collection racine. Vous pourrez aussi lui attribuer un titre.

- Les documents XML/TEI – `data/`. Ce dossier est **obligatoire**. Il contient les sources XML/TEI de votre *<a>projet</a>* organisées selon la hiérarchie de votre choix. Cette hiérarchie représente les collections par défaut de votre *projet*. Par exemple, ici, les documents `file_1.xml` et `file_2.xml` appartiennent à la collection `collection_1`.

- Les métadonnées – `metadata/`. Ce dossier est **optionnel**. S'il est présent, il doit contenir *a minima* un document XML `dots_metadata_mapping.xml` qui permet de déclarer finement où se trouvent les métadonnées de collections et / ou de documents. Ces métadonnées peuvent venir des documents TEI, en déclarant des XPath, mais aussi de fichiers TSV, en l'indiquant dans `dots_metadata_mapping.xml`. Ces fichiers doivent être présents dans le dossier `metadata/`.

- `tei:citeStructure`. L'usage de cet élément TEI ([https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-citeStructure.html](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-citeStructure.html)) est facultatif. Il est cependant nécessaire si vous souhaitez accéder aux fragments de votre choix dans les documents.


## Exemples

La structuration du *dossier de dépôt* reflète la structure éditoriale du *projet*.

À l'intérieur du dossier `data/`, vous pouvez organiser vos documents en collections et sous-collections (ou laisser vos documents "à plat"). Le nom des fichiers est utilisé comme identifiant de la collection. Par défaut, le nom du dossier sert aussi de titre de collection. Il est recommander de déclarer dans un fichier TSV le titre des collections, et éventuellement toutes les métadonnées de votre choix.

Pour les documents, son titre et son identifiant sont par défaut le nom du fichier (sans `.xml`). Si le document TEI dispose d'un attribut `@xml:id` sur l'élément racine `TEI`, c'est cet attribut qui est utilisé comme identifiant.

**Liens au cookbook :**

- [périodiques](cookbook/#publier-un-periodique)
- cartulaire / registre
- théâtre
- correspondance
- roman
- poésie
- dictionnaire


# Chargement (dots) d’un *projet*

## Initialisation de la DB dots


```bash
cd path/to/basex/bin
bash basex ../webapp/dots/scripts/dots_db_init.xq
```

Cette première commande permet d'initialiser la base de données dots. Elle sert à relier chaque ressource identifiée à sa base de données *projet* d'appartenance.

## Création de la base de données *projet*


```bash
cd path/to/basex/bin
bash basex -b dbName=db_name -b projectDirPath=/path/to/dossier/de/depot ../webapp/dots/scripts/project_db_init.xq
```

Cette commande permet de créer automatique la base de données *projet*.
On doit spécifier les arguments suivants :

- `dbName` : nom de la base de données BaseX du *projet*
- `projectDirPath` : chemin absolu vers le *dossier de dépôt* du projet

La base de données *projet* est créée en conservant la structure du paquet de dépôt en collections et sous-collection. 

## Création des registres du *projet*

```bash
bash basex -b dbName=db_name -b topCollectionId=top_collection_id ../webapp/dots/scripts/project_registers_create.xq
```

Cette commande permet de créer les registres dots dans la base de données *projet*. Ce sont ces registres qui fournissent les éléments de réponse au résolveur.

On doit spécifier les arguments suivants :

- `dbName` : nom de la base de données BaseX du *projet*
- `topCollectionId` : identifiant DTS de la collection racine du *projet*

**NB. La base de données du *projet* ne DOIT PAS être ouverte dans le GUI BaseX**.


## Mise à jour du switcher DoTS

```bash
bash basex -b dbName=db_name ../webapp/dots/scripts/dots_switcher_update.xq
```

Le switcher de la base de données DoTS (`dots_db_switcher.xml`) sert à associer les identifiants des ressources (collections et documents) à leur base de données de *projet* d’appartenance.

On doit spécifier l’argument suivant :

- `dbName` : nom de la base de données BaseX du *projet* à parcourir pour mise à jour du switcher. Ainsi, on peut mettre à jour la base pour un unique *projet*.

**NB. La mise à jour du switcher dots doit être réalisée après la création des registres du projet (commande précédente).**

Et voilà. Les ressources de votre projet sont décrites et accessibles via les endpoints DTS fournis par DoTS. La description des réponses d'API est disponible à cette adresse: [résolveur](resolver).


## Créer de nouvelles collections et y attacher des documents (existants)


```bash
bash basex -b srcPath=/path/to/custom_collections.tsv ../webapp/dots/scripts/create_custom_collections.xq 
```

Le fichier ``custom_collections.tsv` illustre comment créer de nouvelles collections et lier des documents (déjà existants) à ces collections.


## Supprimer les registres DoTS d’un projet

Le script `dots_registers_delete.xq` supprime les registres DoTS d’un projet. Dans le même temps, il supprime toutes les entrées correspondant à ce projet dans le switcher DoTS. TODO réécrire.

```bash
bash basex -b dbName=db_name  -b option=true / false../webapp/dots/scripts/dots_registers_delete.xq
```

Cette commande permet de "nettoyer" le switcher de la db `dots` en supprimant toutes les ressources qui appartiennent à la *base de données projet*. Elle permet aussi de supprimer la *base de données projet* si l'option est `true` ; elle se contente sinon de supprimer ses registres dots.

**Attention :** après avoir utilisé cette commande, le résolveur `dots` ne fournit plus de réponse d'API pour ce *projet*.

On doit spécifier les arguments suivants :

- `dbName` : nom de la base de données BaseX du projet à parcourir suppression des registres DoTS.
- `option` : valeur booléenne. `true` permet de supprimer la base de données *projet* et `false` se contente de supprimer les registres `dots` du *projet*. 