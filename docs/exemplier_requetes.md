# Exemplier de requêtes DTS

L’objectif de cette documentation est de **comprendre par l’exemple** les paramètres DTS disponibles et d’appréhender les usages possibles de leurs combinaisons.

!!!warning
	DoTS propose une implémentation de la version [1-alpha](https://distributed-text-services.github.io/specifications/versions/1-alpha/) de DTS.  
    DoTS ne fonctionne que à partir de données XML/TEI et offre par défaut des réponses en TEI.



## Définitions



- Un **projet** est une collection DTS de premier niveau : par exemple, nous distinguons ci-dessous les projets *Théâtre* et *Thèses* qui n’ont aucun rapport éditorial ou thématique.
- Une **collection** est un regroupement éditorial déclaré (thématique, chronologique…) de documents qui peut être hiérarchique (collection de collections). Un même document peut appartenir à différentes collections.
- Pour DoTS, un **document** correspond à un fichier XML/TEI. L’éditeur est invité à définir le découpage éditorial de son corpus en documents : par exemple, dans le cas de la publication d’un périodique, il peut considérer que chaque article est un document (un fichier XML/TEI par article dans ce cas), ou que le volume est un document (un unique fichier XML/TEI pour ce volume, regroupant l’ensemble des articles qui seront alors traités comme des fragments).
- Un **fragment** correspond à un passage déclaré du document. Un fragment peut-être une scène d’une pièce de théâtre, un acte d’un cartulaire, un poème dans un recueil. Les métadonnées de ces fragments sont accessibles grâce au *endpoint* `Navigation`.

## Modèle documentaire

L'essentiel des exemples présentés ci-dessous sont issus du **projet** `theater` dont le modèle documentaire est le suivant :

???+ info "Hiérarchie documentaire" 
    ```  
   
    theatre							collection (collection de premier niveau)
      > moliere						collection
        > moliere_avare 			document
          > actes					fragment
            > scène					fragment
              > tour de parole		fragment
        > moliere_dom-juan          document
        > moliere_tartuffe          document
      > racine                      collection
        > racine_andromaque         documment
        > racine_phedre             document
      > comedie                     collection
        > moliere_avare             document
        > moliere_tartuffe          document
      > tragedie                    collection
        > moliere_dom-juan          document
        > racine_andromaque         document
        > racine_phedre             document

    ```


## *Endpoint* `Collection`

Usages : 

- Lister les membres (collections et documents) d’une collection
- Accéder aux métadonnées d’une collection
- Accéder aux métadonnées d’un document

### Requêtes DTS

Lister les **projets** disponibles : 

> On distingue ici les différents projets (collections de premier niveau) disponibles.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection")
}}

Lister les contenus (collections et/ou documents) du **projet** *theater* et leurs métadonnées : 

> Le projet théâtre comprend 4 collections (`totalChildren`) finement décrites.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=theater")
}}

Lister le contenu de la **collection** "*Trois pièces de Molière*" : 

> Cette collection comprend 3 pièces dont les métadonnées sont listées ici.     
> On constate aussi, d'après le `maxCiteDepth`, que le niveau d’éditorialisation des pièces diffère.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere")
}}

Lister les métadonnées d'un **document** :

> Pour un `id` de **document** (`moliere_avare`), le *endpoint* `Collection` permet ici de lister les métadonnées de ce document.  
> On constate que cette pièce dépend de 2 collections différentes (`totalParents`).

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_avare")
}}

Lister les collections auxquelles le **document** `moliere_avare` appartient : 

> Ici, *L'Avare* est membre des collections *Trois pièces de Molière* et *Les comédies*.  
> Il est possible de changer le "sens de circulation" pour accéder aux informations concernant les parents d'une ressource et non plus ses enfants.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_avare&nav=parents")
}}

### Options DoTS

Lister des **documents** de la **collection** _moliere_ pour lesquels la métadonnée `dc:date` est _1669_ : 

> Un utilisateur peut filtrer des résultats en fonction de la valeur d'une métadonnée de son choix.  
> Le paramètre DoTS `filter` est disponible pour tous les endpoints.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere&filter=dc:date=1669")
}}

## *Endpoint* `Navigation`

Usages :

- Parcourir la structure éditoriale d’un document (la hiérarchie de ses fragments)
- Accéder aux métadonnées des fragments d’un document
- Filtrer la liste des fragments selon leurs métadonnées (fonctionnalité DoTS)

### Requêtes DTS

Lister les **fragments** de niveau 1 (les actes) du **document** `moliere_tartuffe` :

> La première partie de la réponse est un descriptif détaillée de la ressource (ici `moliere_tartuffe`) et particulièrement de sa structure éditoriale.
> La liste des fragments données ensuite est calculée en fonction de la valeur du paramètre `down`.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=1")
}}

Lister les **fragments** de niveau 1 et 2 (les actes et les scènes) du **document** `moliere_tartuffe` :

> Le paramètre `down` permet donc d'afficher les fragments d'un document depuis le niveau 1 **jusqu'au** niveau demandé dans `down`.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=2")
}}

Lister tous les fragments du **document** `moliere_tartuffe` :

> La valeur `-1` permet d'afficher tous les fragments d'un **document**.  
> Ici, `down=4` ou `down=-1` donnent la même réponse.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=-1")
}}

Afficher les métadonnées du **fragment** dont la **référence** est *a3* (acte 3) du **document** `moliere_tartuffe` :

> Le paramètre `ref` permet d'accéder aux métadonnées d'un fragment précis.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3")
}}

Afficher les métadonnées du **fragment** dont la **référence** est *a3* (acte 3) du **document** `moliere_tartuffe` ainsi que la liste de tous les **fragments** qu'il contient et leurs métadonnées :

> Il est possible de combiner les paramètres `ref` et `down`.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3&down=-1")
}}

Dans le **document** `moliere_tartuffe`, lister des **fragments** entre le **fragment** dont la **référence** est *a3-s2* (acte 3, scène 2) et le **fragment** dont la **référence** est *a3-s6* (acte 3, scène 6), et leurs métadonnées :

> Les paramètres `start` et `end` permettent d'accéder à tous les fragments dans un intervalle donné.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&start=a3-s2&end=a3-s6")
}}

<!--
La liste de tous les **fragments** de type _act_ dans **l'arbre de citation** parmi tous les **fragments** du **document** _Le Tartuffe_ de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&tree=act&down=-1")
}}

-->


### Options DoTS

Dans le **document** `moliere_tartuffe`, lister tous les **fragments** de niveau 3 (les tours de parole) dont la métadonnée `tei:role` est *Tartuffe* :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=3&filter=tei:role=Tartuffe")
}}

## *Endpoint* `Document`

Usages :

- Afficher un document complet (XML/TEI ou HTML)
- Afficher un fragment du document 
- Afficher un intervalle de fragments du document 
- Filtrer l’affichage des fragments selon leurs métadonnées (fonctionnalité DoTS)

### Requêtes DTS

Accéder au **document** complet au format XML/TEI : 

> Par défaut, c'est le **document** au format XML/TEI qui est proposé.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe")
}}

Accéder au **document** complet au format HTML : 

> Pour bénéficier d'une version HTML, c'est à l'éditeur de fournir les feuilles de transformation XSLT.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&mediaType=html")
}}

<!--
!!! info "Feuilles de transformation XSLT"

	```
	La réponse au format HTML est disponible sous réserve de déposer sa feuille de transformation XSLT dans le dossier /path/to/basex/webapp/static/transform/{db_name}.
    Le nom de la feuille XSLT doit respecter le nommage suivant : {db_name.xslt}.
	```
-->

Accéder au **fragment** dont la **référence** est *l0012* (niveau 4) du **document** `moliere_tartuffe` au format XML/TEI : 

> On constate que les paramètres `ref`, `start` et `end` sont disponibles pour les endpoints `Navigation` ET `Document`.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&ref=l0012")
}}

Accéder aux **fragments** entre le **fragment** dont la **référence** est *a1-s1_05* (niveau 3) et le **fragment** dont la **référence** est *l0023* (niveau 4) au format XML/TEI : 

> On constate que l'intervalle de fragments demandés peut se faire à partir de fragments de niveaux différents (ici niveaux 3 et 4).

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1-s1_05&end=l0023")
}}

### Options DoTS

Accéder à tous les **fragments** du **document** `moliere_tartuffe` pour lesquels le tour de parole est Tartuffe : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&filter=tei:role=Tartuffe")
}}

Accéder à tous les **fragments** entre l'acte 1 et l'acte 3 du **document** `moliere_tartuffe` dont le tour de parole est celui de *Orgon*, au format HTML : 

> Le paramètre DoTS `filter` peut être combiné avec les autres paramètres DTS (ici avec `start`, `end` et `mediaType`).

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1&end=a3&filter=tei:role=Orgon&mediaType=html")
}}

Accéder au **fragment** dont la référence est *r3587* (Troisième partie) du **document** `ENCPOS_1972_18`, en excluant les **fragments "enfants"** : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=ENCPOS_1972_18&ref=r3587&excludeFragments=true")
}}

Ce tour d'horizon de l'API DTS dans son implémentation DoTS montre qu'il est possible d'accèder très finement aux **documents**, aux **fragments** d'un document et à toutes leurs **métadonnées** grâce aux trois endpoints et à la combinaison de leurs paramètres.
