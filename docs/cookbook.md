# DoTS Cookbook


## Publier un périodique


### Introduction

Cette recette détaille les possibilités offertes par DoTS pour la publication d’un périodique.

Un périodique est une publication régulière et collective, par exemple une revue érudite semestrielle ou les actes annuels d’une conférence.

Nous prenons ici l’exemple de la publication des positions de thèses de l’École des chartes. Une *position* est un résumé de la thèse défendue. Depuis 1849, chaque année un recueil des positions est publié. L’ensemble de ces positions est consultable en ligne : [https://theses.chartes.psl.eu/](https://theses.chartes.psl.eu/).

<!--
```JSON title="https://theses.chartes.psl.eu/dts/collections?id=ENCPOS_1972_18"
--8<-- "https://theses.chartes.psl.eu/dts/collections?id=ENCPOS_1972_18"
```
-->

### Définition du modèle documentaire

[DTS](https://distributed-text-services.github.io/specifications/) permet de décrire et de standardiser l’accès aux :

- collections (`resource @type:Collection`) ;
- documents (`resource @type:Resource`) ;
- passages de ces documents (`fragment`).


La hiérarchie documentaire du corpus des positions est la suivante :

```
racine
	> annee
		> positions
			> sections
```

Pour la gestion et l’édition de vos sources XML/TEI vous pouvez bien entendu organiser le dossier comme bon vous semble.
Mais pour le chargement en base, le dossier de dépôt DoTS explicite vos choix documentaires. Pour la publication d’un périodique,

- les articles (ici les positions de thèse) peuvent être traités comme des documents (cas 1)
- les articles (ici les positions de thèse) peuvent être traités comme le fragment d’un volume (cas 2)


### Cas 1. Un article est un document


Dans ce cas, l’éditeur souhaite mettre l’accent sur la structuration sémantique du corpus : le volume annuel n’est non pas considéré comme un document (un volume), mais comme la collection annuelle des positions publiées.  
Par conséquent, chaque position devient un document de cette collection annuelle.


#### Structure

|unité documentaire|type de resource|data type|(x)path|
|------------------|----------------|---------|----|
|collection des positions|collection|file dir |`data/`|
|volume annuel     |collection      |file dir |`data/ENCPOS_AAAA/`|
|position          |document        |TEI file |`data/ENCPOS_AAAA/ENCPOS_AAAA_NN.xml`|
|section           |fragment        |TEI node |`/TEI/text/boby/div`|



La hiérarchie documentaire est la suivante :

```
encpos							collection (project root)
	> annee						collection
		> positions				document
			> sections			fragment
```


#### Corpus de test

Le corpus de test est disponible : [https://github.com/chartes/dots_documentation/tree/dev/data_test/periodiques/encpos_by_abstract](https://github.com/chartes/dots_documentation/tree/dev/data_test/periodiques/encpos_by_abstract)


!!! info "Structure du dossier de dépôt"

	```
	ENCPOS/								# collection racine
		data/
			ENCPOS_1849/				# collection
				ENCPOS_1849_04.xml		# document
				ENCPOS_1849_08.xml
			ENCPOS_1971/
				ENCPOS_1971_09.xml
				ENCPOS_1971_12.xml
				ENCPOS_1971_14.xml
			…
		metadata/						# métadonnées des collections et des documents
			custom_collections.tsv
			default_collections_titles.tsv
			documents_metadata.tsv
			dots_metadata_mapping.xml
		README.md
	```


#### Dossier `data/`

- Les documents (les fichiers XML/TEI) DOIVENT être regroupés dans un dossier `/data`.
- La structure de ce dossier `/data` permet de représenter les collections **par défaut** du corpus : ici, le document `ENCPOS_1849_04.xml` appartient par défaut à la collection `ENCPOS_1849`.
- Nous verrons qu’un document peut appartenir à plusieurs collections.


#### Dossier `metadata/`

Ce dossier est facultatif.

Il contient les métadonnées descriptives des ressources : `default_collections_titles.tsv` pour la description des collections et `documents_metadata.tsv` pour la description des documents.

Le fichier `dots_metadata_mapping.xml` est important. Il permet de :

- lister et qualifier les métadonnées partagées via le endpoint DTS Collections ;
- déclarer leur localisation.

Ces métadonnées peuvent être inscrites dans la source XML/TEI, généralement dans le `teiHeader`. Dans ce cas, la localisation est inscrite en valeur de l’attribut `@xpath`.

Ces métadonnées peuvent être déportées dans un tableur CSV (`@source`). Dans ce cas, la localisation est inscrite en valeur de l’attribut `@value`.

Exemples :

- le titre (`dc:title`) de chaque document du projet :

```xml
<dc:title
  xpath="//titleStmt/title[@type='main' or position()=1]"
  scope="document"/>
```

- le titre (`dc:title`) de chaque collection du projet :

```xml
<dc:title
  format="csv"
  source="./default_collections_titles.tsv"
  resourceId="id"
  value="title"
  scope="collection"/>
```

> NB1. Il est recommandé de fournir a minima un CSV avec le titre des collections (ici `default_collections_titles.tsv`).  
> NB2. Si aucune métadonnée n’est fournie, DoTS utilise le nom du dossier (qui sert aussi d’identifiant de collection) comme titre de collection.


#### Déclaration des fragments

L'élément `<citeStructure>` ( [https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-citeStructure.html](https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-citeStructure.html) ) est facultatif.
Il permet de déclarer la structure du document TEI et de retrouver des fragments.

Exemple d'une structure hiérarchique d'un document à un niveau (un chapitre = un fragment) :

```xml
<encodingDesc>
  <refsDecl>
    <citeStructure unit="chapter" match="/TEI/text/body/div" use="position()">
      <citeData use="head" property="dc:title"/>
    </citeStructure>
  </refsDecl>
</encodingDesc>
```


#### Ajout d’une collection thématique

Dans un second temps, il est possible de créer de nouvelles collections et de lier des documents déjà présents dans la base à ces collections nouvellement créées.
Ainsi, un même document peut appartenir à plusieurs collections.

Il est nécessaire pour cela de préparer un tableur TSV sur le modèle de `custom_collections.tsv`.

```
bash basex -b srcPath=/path/to/csv ../webapp/dots/scripts/create_custom_collections.xq 
```

Argument à spécifier pour lancer la commande :

- `srcPath` : chemin vers le tableur TSV


### Cas 2. Un article est un fragment

Dans ce cas, l’éditeur souhaite mettre l’accent sur la structuration matérielle du corpus : chaque année est un tome considéré comme un document (un volume).  
Par conséquent, chaque position devient un fragment de ce document.

#### Structure


La hiérarchie documentaire est la suivante :

```
encpos							collection
	> annee						document
		> positions				fragment
			> sections			fragment
```

Il convient de déclarer chacune de ces unités documentaires.

|unité documentaire|type de resource|data type|(x)path|
|------------------|----------------|---------|----|
|collection des positions|collection|file dir |`data/`|
|volume annuel     |document        |TEI file |`data/ENCPOS_AAAA.xml/`|
|position          |fragment        |TEI node |`/TEI/text/boby/div[@type='position]'`|
|section           |fragment        |TEI node |`/TEI/text/boby/div[@type='position]/div`|


**Collections**. Il suffit d’organiser le dossier `data/` en collections et sous-collections par défaut. Les métadonnées peuvent être déportées dans un CSV (ici `titles.tsv`).

**Documents**. Les documents correspondent aux fichiers XML/TEI.

**Fragments**. La hiérarchie des fragments est déclarée, pour chaque document, grâce à l’élément `citeStructure` du `teiHeader` :

```xml
<encodingDesc>
  <refsDecl>
    <citeStructure unit="position" match="/TEI/text/body/div[@type='position']" use="@xml:id">
      <citeData use="head" property="dc:title"/>
      <citeStructure unit="chapter" match="div" use="position()">
        <citeData use="head" property="dc:title"/>
      </citeStructure>
    </citeStructure>
  </refsDecl>
</encodingDesc>
```


#### Corpus de test

Le corpus de test : [https://github.com/chartes/dots_documentation/tree/dev/data_test/periodiques/encpos_by_volume](https://github.com/chartes/dots_documentation/tree/dev/data_test/periodiques/encpos_by_volume)

```
Dir Project (exemple: ENCPOS)

  > /positions_by_volume (collection - projet)
    >/data
      > /ENCPOS_1849_c2.xml (document)
      > /ENCPOS_1971_c2.xml (document)
      > /ENCPOS_1972_c2.xml (document)
    > /metadata
      > dots_metadata_mapping.xml
      > encpos.tsv
      > titles.csv
```

#### Dossier `data/`

Le dossier `/data` regroupe les fichiers TEI de la collection projet : ici, le document ENCPOS_1849.xml, par exemple, regroupe toutes les positions de 1849.
Chaque position est dans ce cas un fragment du document.

#### Dossier `metadata/`

Ce dossier contient les métadonnées descriptives des documents: le document `default_resources_titles.tsv` permet de lister les titres de la collection racine et des documents.

#### Déclaration des fragments

L'élément `<citeStructure>` ( [https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-citeStructure.html](https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-citeStructure.html) ) est utilisé pour déclarer la structure d'un document.
  Il est possible, comme dans cet exemple, de déclarer une structure imbriquée: les chapitres dans les positions de thèse.

```xml
<refsDecl>
  <citeStructure unit="position" match="/TEI/text/body/div[@type='position']" use="@xml:id">
    <citeData use="head" property="dc:title"/>
    <citeStructure unit="chapter" match="div" use="position()">
      <citeData use="head" property="dc:title"/>
    </citeStructure>
  </citeStructure>
</refsDecl>
```