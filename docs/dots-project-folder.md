# Le dossier de dépôt

Le dossier de dépôt est le dossier chargé en base grâce aux modules DoTS et contenant les sources XML/TEI publiées.

Pour tirer avantage de l’ensemble des outils de la suite DoTS, votre dossier de dépôt doit se conformer aux recommandations détaillées dans ce document.

Ce document détaille en particulier les règles de structuration de ce dossier de dépôt ainsi que les méthodes disponibles pour déclarer les métadonnées des ressources publiées (collections, documents et fragments).

Des [cookbooks](./cookbook.md) illustrent la mise en œuvre de ces recommandations, pour différents types de publication, genres littéraires et choix documentaires.


## Structure du dossier de dépôt

???+ info "Modèle"

	```
	nom_projet/							# Racine du dossier de dépôt
		data/							# OBLIGATOIRE. Fichiers TEI en dossiers de collection
			collection_1/				# Collection 1
				file_1.xml				# file_1 appartient par défaut à la collection 1
				file_2.xml				# idem
			collection_2/				# Collection 2
				file_100.xml			# file_100 appartient par défaut à la collection 2
				file_101.xml			# idem
		metadata/						# OPTIONNEL. Métadonnées des collections et des documents
			dots_metadata_mapping.xml	# Déclaration du chemin des métadonnées
			metadata_1.tsv				# Un fichier de métadonnées
			metadata_2.tsv				# idem
		README.md						# OPTIONNEL. Documentation (plan de nommage, etc.)
	```


- `nom_projet/`: racine du dossier de dépôt. Son nom est libre. Au chargement en base, vous pourrez spécifier le nom de la base de données BaseX, ainsi que l’identifiant DTS attribué à la collection racine. Vous pourrez aussi lui attribuer un titre.

- `data/`: les documents XML/TEI. Ce dossier est **obligatoire**. Il contient les sources XML/TEI de votre projet organisées selon la hiérarchie de votre choix. Cette hiérarchie représente les collections par défaut de votre projet. Par exemple, ici, les documents `file_1.xml` et `file_2.xml` appartiennent à la collection `collection_1`.

- `metadata/`: les métadonnées. Ce dossier est **optionnel**. Si présent, il doit contenir *a minima* le document XML `dots_metadata_mapping.xml` qui permet de déclarer l’accès aux métadonnées des collections et/ou des documents. 


## Déclarer la structure éditoriale du projet


### Collections par défaut

La structuration du dossier `data/` représente la structure éditoriale du projet.

Vous pouvez structurer vos documents en collections et sous-collections hiérarchiques (ou tous les déposer "à plat" en racine du dossier).


??? example "Le projet contient une unique collection racine"

	```
	moliere_project/
		data/
			avare.xml
			scapin.xml
			tartuffe.xml
	```

??? example "Le projet contient des sous-collections"

	```
	theater_project/
		data/
			corneille/
				cid.xml
				horace.xml
			moliere/
				avare.xml
				scapin.xml
				tartuffe.xml
	```

??? example "Le projet contient des sous-sous-collections, etc."

	```
	theater_project/
		data/
			corneille/
				cid.xml
				horace.xml
			moliere/
				ballet/
					psyche.xml
				comedy/
					avare.xml
					scapin.xml
					tartuffe.xml
	```



#### Id et titre des collections

**Le nom du dossier de collection est retenu comme identifiant de la collection.**  
Il est donc recommandé de ne pas utiliser d’espace ou de diacritique pour le nommage de ces dossiers. Un plan de nommage de ces dossiers de collection peut utilement documenter un dossier de dépôt dans le `README.md`.

Par défaut, le nom des dossiers de collection sert aussi de titre (`dc:title`). Il est recommandé de déclarer dans un fichier TSV le titre des collections (ainsi que toutes les métadonnées utiles à leur description).


#### Id et titre des documents

Pour un document, l’identifiant retenu par ordre de priorité est :

1. la valeur de l’attribut `@xml:id` de la racine `TEI` du fichier si elle est renseignée ;
1. le nom du fichier (sans l’extension `.xml`).


Pour un document, le titre (`dc:title`) retenu par ordre de priorité est :

1. la valeur renseignée dans `dots_metadata_mapping.xml` (optionnel) ;
1. la valeur renseignée dans le `teiHeader`, par défaut `titleStmt/title` (optionnel) ;
1. le nom du fichier (sans l’extension `.xml`).


### Autres collections

Avec DoTS, un même document peut-être assignés à différentes collections.

La description de ces nouvelles collections – avec la liste de leurs documents – doit être structurée dans un TSV conforme au modèle suivant.



| |dbName|collectionId|title|parentId|documentIds|description|
|-|------|------------|-----|---------|-----------|-----------|
|**Description**|nom de la db|id de la collection|`dc:title`|id de la collection parente|liste des ids des documents|`dc:description`|
|**Example**|theater|comedy|Les comédies classiques|theatre-genre|avare\|illusion-comique\|plaideurs|Les comédies de Corneille, Molière et Racine|
	



### Passages


Le endpoint `Navigation` permet de lister les passages référencés d’un document. Le enpoint `Document` permet d’en afficher le contenu.

Ce découpage éditorial optionnel d’un document est déclaré dans son `teiHeader` grâce à l’élément [`citeStructure`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-citeStructure.html).

Cette déclaration est **optionnelle**.


???+ example "Example de `tei:citeStructure` pour une pièce de théâtre"

	```xml
	<citeStructure match="//div[@type='act']" use="@xml:id" unit="act">
		<citeData use="head" property="dc:title"/>
		<citeStructure match="div[@type='scene']" use="@xml:id" unit="scene">
			<citeData use="head" property="dc:title"/>
			<citeStructure match="sp" use="position()" unit="speaker">
				<citeData use="substring-after(@who, '#')" property="dc:title"/>
				<citeStructure match="l" use="@xml:id" unit="verse"/>
			</citeStructure>
		</citeStructure>
	</citeStructure>
	```



## Déclarer les métadonnées des ressources du projet

### Métadonnées obligatoires

**Pour une collection et un document**, DTS impose la déclaration d’un identifiant et d’un titre. Cependant, pour publier un projet, DoTS n’a besoin d’aucune métadonnée et attribue automatiquement aux ressources un identifiant et un titre défini selon cet ordre de priorité.

Identifiant de collection :

1. nom du dossier de collection dans `data/`

Titre de collection (`dc:title`) :

1. valeur référencée dans `metadata/dots_metadata_mapping.xml` (voir surcharge)
1. nom du dossier de collection dans `data/`

Identifiant de document :

1. valeur de l’attribut `/TEI/@xml:id` du fichier
1. nom du fichier (sans l’extension `.xml`)

Titre de document (`dc:title`) :

1. valeur référencée dans `metadata/dots_metadata_mapping.xml` (voir surcharge)
1. valeur de `/TEI/teiHeader/fileDesc/titleStmt/title[@type='main']`
1. valeur de `/TEI/teiHeader/fileDesc/titleStmt/title[1]`
1. nom du fichier (sans l’extension `.xml`)


**Pour un passage**, DTS impose la déclaration d’un identifiant. DoTS attribue automatiquement aux passages un identifiant selon la déclaration faite par l’éditeur dans l’élément `citeStructure`. L’identifiant est copié ou calculé selon la valeur de l’attribut `citeStructure/@use`.

!!! warning

    Pour l’attribution des identifiants de passage déclarés en valeur de `citeStructure/@use`, DoTS prends en charge la **seule** valeur `@xml:id`, qui garantit l’unicité de cette identification des passages dans le document. DoTS ne traite pas les autres valeurs possibles de `@use`, telles que `position()` ou `@n`, et attribue automatiquement un identifiant aux passages selon leur ordre d’inscription dans le registre DoTS.





### Surcharge et métadonnées optionnelles

Pour les collections et les documents, le fichier `metadata/dots_metadata_mapping.xml` permet :

- de surcharger le titre (`dc:title`) attribué par défaut par DoTS ;
- d’appeler optionnellement toutes les métadonnées souhaitées. Et ces métadonnées peuvent être inscrites dans le `teiHeader` des documents et/ou déportées dans un tableur.


!!! example "dots_metadata_mapping.xml"

	```xml
	<?xml version="1.0" encoding="UTF-8"?>
	<metadataMap xmlns="https://github.com/chartes/dots/"
	  xmlns:dc="http://purl.org/dc/elements/1.1/"
	  xmlns:dct="http://purl.org/dc/terms/"
	  xmlns:html="http://www.w3.org/1999/xhtml">
	  <mapping>
	    <dct:license scope="collection" resourceId="all" value=".">https://creativecommons.org/licenses/by/4.0/</dct:license>
	    <dc:title  scope="collection" format="csv" source="./default_collections_titles.tsv" resourceId="id" value="title"/>
	    <dct:license scope="document" resourceId="all" value=".">https://creativecommons.org/licenses/by-nc-sa/4.0/</dct:license>
	    <dc:title scope="document" xpath="//titleStmt/title[@type = 'main' or position() = 1]"/>
	    <html:h1 scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="title_rich"/>
	    <dc:date  scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="promotion_year" type="number"/>
	    <dc:creator scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="author_fullname_label"></dc:creator>
	    <dct:creator scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="author_idref_ppn" prefix="https://www.idref.fr/" key="@id"/>
	    <dct:creator scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="author_dbpedia_id" prefix="https://dbpedia.org/resource/" key="@id"/>
	    <dct:isVersionOf scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="sudoc_these-record_ppn" prefix="https://www.sudoc.fr/" key="@id"/>
	    <dct:extent scope="document" format="csv" source="./documents_metadata.tsv" resourceId="id" value="pagination"/>
	  </mapping>
	</metadataMap>
	```

Pour déclarer une métadonnée, il suffit de l’élément avec le préfixe permettant de qualifier son vocabulaire d’appartenance.

L’attribut `@scope` permettent de spécifier le type de ressource décrit.

`@scope`:

- déclarer les ressources décrites.
- valeurs autorisées: `collection`,`document`


Ces métadonnées peuvent être inscrites :

- dans le fichier `dots_metadata_mapping.xml` pour les valeurs communes à l’ensemble des collections ou à l’ensemble des documents.
- dans un fichier TSV (pour les collections et les documents)
- dans le fichier XML/TEI (pour les seuls documents)



#### Métadonnées inscrites dans `dots_metadata_mapping.xml`

Certaines métadonnées, telle qu’une licence, peuvent être partagées par l’ensemble des ressources. Dans ce cas, leur valeur peut être renseignée directement dans `dots_metadata_mapping.xml`.


!!! abstract "Template"

	```xml
	<ns:property
		scope="collection|document"
		resourceId="all"
		value=".">property value</ns:property>
	```


!!! example "Exemple. Déclaration d’une licence commune à tous les documents"

	```xml
	<dct:license
		scope="document"
		resourceId="all"
		value=".">https://creativecommons.org/licenses/by-nc-sa/4.0/</dct:license>
	```

|attribut|définition|valeur|commentaire|
|--------|----------|------|-----------|
|`@scope`|type des ressources décrites|`collection` ou `document`||
|`resourceId`|ids des ressources décrites|`all`|la métadonnée décrit toutes les ressources d’un type|
|`value`|emplacement de la valeur|`.`|la valeur de la métadonnée correspond au contenu de l’élément|

<!--
**Modèle**
```xml
<ns:property scope="collection|document" resourceId="all" value=".">property value</ns:property>
```

- `<propriété/>` : le nom de l'élément permet de définir la propriété attendue en réponse de la requête API. Dans l'exemple, la propriété est la licence en dublin core.
- `@scope` : la valeur attendue est *collection* ou *document*, selon la porté de la métadonnée.
- `@resourceID` : la valeur doit être ici *all* pour spécifier que la métadonnée concerne l'ensemble des ressources (collection ou document).
- le contenu de l'élément correspond à la valeur attendue pour la réponse d'API.
-->



#### Métadonnées déportées dans un tableur TSV

Les métadonnées des documents et des collections peuvent être déportées dans un tableur. `dots_metadata_mapping.xml` permet de les appeler.

!!! abstract "Template"

	```xml
	<ns:property
		scope="collection|document"
		format="tsv"
		source="path/to/tsv_file"
		resourceId="resourceId_column-header"
		value="value_column-header"/>
	```


!!! example "Exemple. Appel des dates de publication (`dc:date`) des documents"

	```xml
	<dc:date 
		scope="document" 
		format="tsv"
		source="./documents_metadata.tsv"
		resourceId="doc_id" 
		value="publication_year"/>
	```

!!! example "Exemple. `documents_metadata.tsv`"

	|doc_id|titre|publication_year|
	|------|-----|----------------|
	|ENCPOS_1849_08|Wala et Louis le Débonnaire|1849|
	|ENCPOS_1971_14|Le bestiaire héraldique au Moyen Âge|1972|


|attribut|définition|valeur|commentaire|
|--------|----------|------|-----------|
|`@scope`|type des ressources décrites|`collection` ou `document`||
|`@format`|format du fichier de métadonnées appelé|`tsv`||
|`@source`|chemin vers le fichier de métadonnées|`path/to/file`||
|`@resourceId`|nom de la colonne référençant l’id de la ressource décrite|||
|`@value`|nom de la colonne contenant la valeur de la métadonnée|||



#### Métadonnées inscrites dans la source XML/TEI

Les métadonnées d’un document peuvent être inscrites dans son teiHeader. `dots_metadata_mapping.xml` permet de les appeler et spécifiant un chemin XPath.


!!! abstract "Template"

	```xml
	<ns:property
		scope="document" 
		xpath="xpath/to/metadata"/>
	```


!!! example "Exemple. Appel du titre (`dc:title`) des documents"

	```xml
	<dc:title 
		scope="document" 
		xpath="//titleStmt/title[@type = 'main' or position() = 1]"/>
	```

|attribut|définition|valeur|commentaire|
|--------|----------|------|-----------|
|`@scope`|type des ressources décrites|`document`||
|`@xpath`|chemin de la métadonnée|||


#### Synthèse

TODO Tableau récap (après validation des précédents)

D'autres fonctionnalités sont par ailleurs disponibles dans tous les cas de figure.
Il est notamment possible de typer les métadonnées : l'attribut `@type` peut prendre la valeur *number* ou *boolean* selon les besoins.
**NB. Attention cependant: si la valeur ne correspond pas au type demandé, la réponse d'API affiche une erreur.**
Enfin, un mécanisme de préfixage et de suffixage est disponible pour compléter au besoin les métadonnées des TSV. Les attributs `@prefix` et `@suffix` peuvent être utilisés.
