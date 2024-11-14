# Publier des cartulaires


## Introduction

Cette recette détaille les possibilités offertes par DoTS pour la publication de cartulaires.

L’objectif est de pouvoir décrire, citer et republier :

- un texte introductif (paratexte),
- un acte

Nous prenons ici l'exemple de cartulaires issus des <a href="http://elec.enc.sorbonne.fr/cartulaires/" target="_blank">Cartulaires d'Île de France</a>.

## Définition du modèle documentaire

<a href="https://distributed-text-services.github.io/specifications/" target="_blank">DTS</a> permet de décrire et de standardiser l’accès aux :

- collections (`resource @type:Collection`) ;
- documents (`resource @type:Resource`) ;
- passages de ces documents (`fragment`).


La hiérarchie documentaire du corpus des cartulaires est la suivante :

???+ info "Modèle"

    ```
      > cartulaire
        > paratexte
          > partie
            > sous-partie ?  
        > acte
    ```

Pour la gestion et l’édition de vos sources XML/TEI, vous pouvez bien entendu organiser votre dossier de travail comme bon vous semble.

Mais pour le chargement en base, le dossier de dépôt DoTS explicite vos choix documentaires. Nous faisons ici le choix de proposer un projet sans collection, avec un set de fichiers TEI.


## Structure du dossier de dépôt


???+ info "Hiérarchie documentaire"

    ```
    cartulaires						collection (collection de premier niveau)
      > cartulaire				    document
        > paratexte					fragment
          > partie					fragment
            > sous-partie			fragment
        > acte				        fragment
    ```

Il convient de déclarer chacune de ces unités documentaires.

| unité documentaire         |type de resource|data type| (x)path                                   |
|----------------------------|----------------|---------|-------------------------------------------|
| collection des cartulaires |collection      |file dir | `data/`                                   |
| cartulaire                 |document        |TEI file | `data/nom-cartulaire.xml`                 |
| paratexte                  |fragment        |TEI node | `/TEI/text/front`                         |
| partie                     |fragment        |TEI node | `/TEI/text/front/div[@xml:id]`            |
| sous-partie                |fragment        |TEI node | `/TEI/text/front/div[@xml:id]/div[@type]` |
| acte                       |fragment        |TEI node | `/TEI/text/group/group/text[@xml:id]`     |


## Corpus de test

Le corpus de test est disponible : <a href="https://github.com/chartes/dots_documentation/tree/dev/data_test/cartulaires" target="_blank">https://github.com/chartes/dots_documentation/tree/dev/data_test/cartulaires</a>.

!!! info "Structure du dossier de dépôt"

	```
	cartulaires/							# collection de premier niveau
		data/
            Maintenon.xml   			    # document
            S-Germain-en-Laye.xml           # document
            S-Gondon.xml                    # document
		README.md
	```


### Dossier `data/`

- Les documents (les fichiers XML/TEI) **doivent** être regroupés dans un dossier `/data`.
- La structure de ce dossier `/data` permet de représenter les collections par défaut du corpus : ici, les cartulaires ne sont pas organisées en collection.

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=cartulaires")
}}

### Dossier `metadata/`

Ce dossier est facultatif. Il contient les métadonnées descriptives des ressources (collections, documents et fragments).

Le cas échéant, le fichier `dots_metadata_mapping.xml` permet de déclarer les métadonnées associées aux différentes ressources.

Ici, aucune métadonnée ne provient de fichiers TSV externes. Ce dossier n'est donc pas présent pour le présent exemple.

### Déclarer les fragments

L'élément <a href="https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-citeStructure.html" target="_blank">`<citeStructure>`</a> permet de déclarer la structure éditoriale du document TEI et de retrouver des fragments. Pour DoTS, Il est facultatif.

Cependant, dans le cas d’une édition théâtrale, sa déclaration permet de tirer parti du balisage éditorial XML/TEI. Grâce à DTS, chaque acte, scène, tour de parole, vers peut être cité et republié.

Prenons l’exemple de *Phèdre* de Racine. La structure imbriquée du `citeStructure` rend compte de la hiérarchie éditoriale : acte > scène > tour de parole > vers.

???+ example "Déclaration de la structure éditoriale de *Phèdre* de Racine"

    ```XML
    <!--(1)-->
    <citeStructure match="/TEI/text/body/div[@type='acte']" use="@xml:id" unit="act">
      <citeData use="head" property="dc:title"/>
      <!--(2)-->
      <citeStructure match="div[@type='scene']" use="@xml:id" unit="scene">
        <citeData use="head" property="dc:title"/>
        <citeData use="stage" property="tei:castList"/>
        <!--(3)-->
        <citeStructure match="sp" use="@xml:id" unit="individual_speech">
          <citeData use="substring-after(@who, '#')" property="tei:role"/>
          <!--(4)-->
          <citeStructure match="l" use="@xml:id" unit="verse">
            <citeData use="@n" property="tei:num"/>
          </citeStructure>
        </citeStructure>
    </citeStructure>
    </citeStructure>
    ```

    1. Un acte correspond (`@match`) à chaque `div[@type='acte']`. Il est identifié (`@use`) grâce aux `@xml:id` de ces `div`. Son titre (`citeData[@property='dc:title']` correspond (`@use`) à la valeur de son élément `head`. Un acte contient des scènes.
    2. Une scène correspond (`@match`) à chaque `div[@type='scene']`. Elle est identifiée (`@use`) grâce aux `@xml:id` de ces `div`. Son titre (`citeData[@property='dc:title']` correspond (`@use`) à la valeur de son élément `head`. Ici, on extrait aussi la liste des personnages impliqués (`citeData[@property='tei:castList']`). Une scène contient des tours de parole.
    3. Un tour de parole correspond (`@match`) à chaque `sp`. Il est identifié (`@use`) grâce aux `@xml:id` de ces `sp`. Pas de titre, mais un locuteur (`citeData[@property='tei:role']`). Un tour de parole contient des vers.
    4. Un vers correspond (`@match`) à chaque `l`. Il est identifié (`@use`) grâce aux `@xml:id` de ces `l`. Son numéro (`citeData[@property='tei:num']` correspond (`@use`) à la valeur de son attribut `@n`.


Une structure documentaire déclarée peut avoir plusieurs métadonnées. Ici, une scène (`citeStructure match="div[@type='scene']`) a un titre (`citeData[@property="dc:title"]`) et une liste de personnages (`citeData[@property="tei:castList"]`).

#### XQuery

Les *Guidelines TEI* précisent que la valeur attendue de l’attribut <a target="_blank" href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.citeStructurePart.html">`@use`</a> de l’élément <a target="_blank" href="https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-citeData.html">`citeData`</a> est une expression XPath pointant vers la valeur de la métadonnée définie.

Prenons l’exemple des tours de parole (`sp`) de *Phèdre* :

```XML
<citeData use="substring-after(@who, '#')" property="tei:role"/>
```

En valeur de l’attribut `@use`, l’XPath permet d’extraire le nom du locuteur.

En TEI, il est possible de déporter la liste des personnages et leur description dans un élément `castList`. Par exemple, dans l’édition de *Tartuffe* de Molière, les personnages sont listés en début de fichier : chaque personnage est ainsi identifié (`castItem/role/@xml:id`) et décrit, avec un lien à l’autorité Wikidata (`name/@ref`).

```XML
<castList>
  <castItem><role xml:id="cleante"><name ref="https://www.wikidata.org/wiki/Q63492377">Cléante</name></role>, Beau-frère d’Orgon.</castItem>
  <castItem><role xml:id="tartuffe"><name ref="https://www.wikidata.org/wiki/Q63492366">Tartuffe</name></role>, Faux Dévot.</castItem>
  <castItem><role xml:id="dorine"><name ref="https://www.wikidata.org/wiki/Q63492374">Dorine</name></role>, Suivante de Mariane.</castItem>
</castList>
```

Dans l’édition, le locuteur de chaque tour de parole est ensuite identifié en référence à cette liste (`sp/role/@who`), par exemple pour une réplique de Tartuffe :

```XML
<sp who="#tartuffe" xml:id="a3-s2_03">
  <speaker>Tartuffe</speaker>
  <l n="858" xml:id="l0858">Que voulez-vous ?</l>
</sp>
```

DoTS est capable d’interpréter en valeur de `@use` une expression XQuery de manière à accéder depuis un tour de parole à la description du locuteur déportée dans le `castList` en tête de fichier. Ici, pour le locuteur, on appelle la valeur du `castList/castItem/role` lui correspondant.


```XML
<citeStructure match="sp" use="@xml:id" unit="individual_speech">
  <citeData
    property="tei:role"
    use="let $w := substring-after(@who, '#') let $r := ancestor::TEI/text/front/div/castList/castItem/role[@xml:id = $w] return $r"
  />
</citeStructure>
```

Il est bien sûr possible de conserver aussi le liage Wikidata pour l’identification des personnages.

```XML
<citeStructure match="sp" use="@xml:id" unit="individual_speech">
  <citeData
    property="tei:role"
    use="let $w := substring-after(@who, '#') let $r := ancestor::TEI/text/front/div/castList/castItem/role[@xml:id = $w] return $r"
  />
  <citeData
    property="character_QID"
    use="let $w := substring-after(@who, '#') let $r := ancestor::TEI/text/front/div/castList/castItem/role[@xml:id = $w]/name/@ref return $r"
  />
</citeStructure>
```

Ces métadonnées – label et liage Wikidata du locuteur – sont ainsi accessibles via DTS, par exemple pour lister tous les tours de parole de la deuxième scène du troisième acte, avec leur locuteur :


{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3-s2")
}}


## Créer la base de données

Pour créer la base de données, il suffit de saisir la commande :

```bash
bash project_create.sh
	--project_dir_path 'path/to/dots_documentation/data_test/theatre'
	--top_collection_id 'theater'
	--db_name 'theater'
```


## Ajout d’une collection thématique

Un document peut appartenir à plusieurs collections.

Il est possible de créer de nouvelles collections et de lier des documents déjà présents dans la base à ces collections nouvellement créées.

Il est nécessaire pour cela de préparer un tableur TSV sur le modèle de `custom_collections.tsv` :


|dbName|collectionId|dc:title|documentIds|dc:description|
|------|------------|--------|-----------|--------------|
|theater|comedie|Les comédies|moliere_avare\|moliere_tartuffe|Collection thématique des comédies|
|theater|tragedie|Les tragédies|moliere_dom-juan\|racine_phedre\|racine_andromaque|Collection thématique des tragédies|


Puis de lancer la commande suivante.

Argument à spécifier :

- `collections_tsv_path` : chemin absolu vers le fichier TSV de métadonnées de collections

```{.Bash .copy} 
bash custom_collections.sh --collections_tsv_path path/to/tsv/file
```

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=comedie")
}}

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_tartuffe&nav=parents")
}}


## Filtrer les fragments

Le paramètre optionnel DoTS de requête permet de filtrer une liste de membres en utilisant les métadonnées disponibles.

Quelques exemples :

**Les pièces de Molière datées de 1669**

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere&filter=dc:date=1669")
}}


**Les références de tous les tours de parole (passages de niveau 3) de Tartuffe**

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=3&filter=tei:role=Tartuffe")
}}

**Le texte de tous les tours de parole de Tartuffe**

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&filter=tei:role=Tartuffe")
}}


**Le texte de tous les tours de parole de Tartuffe en HTML pour republication**

{{ macro_collapse_card_api_doc(
  verb_http="get", 
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&filter=tei:role=Tartuffe&mediaType=html")
}}

!!! warning

	Pour bénéficier d'une version HTML d'un document ou d'un fragment, il est indispensable de fournir une feuille XSLT dans le dossier `path/to/basex/webapp/static/transform/hteiml`. Le chemin peut être modifié en changeant la variable `$G:xsl` du fichier `globals.xqm`. Le nom de la feuille XSLT doit être `tei2html.xsl`.
