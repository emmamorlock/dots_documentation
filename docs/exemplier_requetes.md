# Exemplier de requêtes DTS

L’objectif de cette documentation est de **comprendre par l’exemple** les paramètres DTS disponibles et d’appréhender les usages possibles de leurs combinaisons.

!!!warning
	DoTS propose une implémentation de la version [1-alpha](https://distributed-text-services.github.io/specifications/versions/1-alpha/) de DTS.


## Définitions



- Un **projet** est une collection DTS de premier niveau : par exemple, nous distinguons ci-dessous les projets *Théâtre* et *Thèses* qui n’ont aucun rapport éditorial ou thématique.
- Une **collection** est un regroupement éditorial déclaré (thématique, chronologique…) de documents qui peut être hiérarchique (collection de collections). Un même document peut appartenir à différentes collections.
- Pour DoTS, un **document** correspond à un fichier XML/TEI. L’éditeur est invité à définir le découpage éditorial de son corpus en documents : par exemple, dans le cas de la publication d’un périodique, il peut considérer que chaque article est un document (un fichier XML/TEI par article dans ce cas), ou que le volume est un document (un unique fichier XML/TEI pour ce volume, regroupant l’ensemble des articles qui seront alors traités comme des fragments).
- Un **fragment** correspond à un passage déclaré du document. Un fragment peut-être une scène d’une pièce de théâtre, un acte d’un cartulaire, un poème dans un recueil. Les métadonnées de ces fragments sont accessibles grâce au *endpoint* `Navigation`.

## *Endpoint* `Collection`

Usages : 

- Lister les membres (collections et documents) d’une collection
- Accéder aux métadonnées d’une collection
- Accéder aux métadonnées d’un document

### Requêtes DTS

Lister les **projets** disponibles : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection")
}}

Lister les contenus (collections et/ou documents) du **projet** *theater* et leurs métadonnées : 

> Le projet théâtre comprend 4 collections (`totalChildren`) finement décrites.  
> NB. Une même pièce peut appartenir à plusieurs de ces collections (voir plus bas).

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=theater")
}}

Lister le contenu de la **collection** "*Trois pièces de Molière*" : 

> Cette collection comprend 3 pièces dont les métadonnées sont listées ici.  
> On constate ici que le niveau d’éditorialisation des pièces diffère (`maxCiteDepth`, voir…)  
> On constate encore que chacune de ces pièces dépend de 2 collections différentes (`totalParents`)

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere")
}}

Lister les métadonnées du **document** *L'avare* de Molière :

> Pour un `id` de **document** (`moliere_avare`), le *endpoint* `Collection` permet ici de lister les métadonnées de ce document.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_avare")
}}

La liste des collections auxquelles le **document** *Le Tartuffe* de Molière appartient : 

> On observe qu’un même document peut être associé à différentes collections. *Le Tartuffe* est ici membre des collections *Trois pièces de Molière* et *Les comédies*.

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_tartuffe&nav=parents")
}}

### Options DoTS

La liste des **documents** de la **collection** _Molière_ pour lesquels la métadonnée `dc:date` est _1669_ : 

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

La liste des **fragments** de niveau 1 (les actes) du **document** *Le Tartuffe* de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=1")
}}

La liste des **fragments** de niveau 1 et 2 (les actes et les scènes) du **document** *Le Tartuffe* de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=2")
}}

La liste de tous les fragments du **document** *Le Tartuffe* de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=-1")
}}

Les métadonnées du **fragment** dont la **référence** est *a3* (acte 3) du **document** *Le Tartuffe* de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3")
}}

Les métadonnées du **fragment** dont la **référence** est *a3* (acte 3) du **document** *Le Tartuffe* de Molière ainsi que la liste de tous les **fragments** qu'il contient avec leurs métadonnées :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3&down=-1")
}}

La liste des **fragments** entre le **fragment** dont la **référence** est *a3-s2* (acte 3, scène 2) et le **fragment** dont la **référence** est *a3-s6* (acte 3, scène 6), et leurs métadonnées :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&start=a3-s2&end=a3-s6")
}}

La liste de tous les **fragments** de type _act_ dans **l'arbre de citation** parmi tous les **fragments** du **document** _Le Tartuffe_ de Molière :

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&tree=act&down=-1")
}}


### Options DoTS

Tous les **fragments** de niveau 3 (les tours de parole) dont la métadonnée `tei:role` est *Tartuffe* :

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

Le **document** complet au format XML/TEI : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe")
}}

Le **document** complet au format HTML : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&mediaType=html")
}}

!!! info "Feuilles de transformation XSLT"

	```
	La réponse au format HTML est disponible sous réserve de déposer sa feuille de transformation XSLT dans le dossier /path/to/basex/webapp/static/transform/{db_name}.
    Le nom de la feuille XSLT doit respecter le nommage suivant : {db_name.xslt}.
	```


Le **fragment** dont la **référence** est *l0012* (niveau 4) du **document** *Le Tartuffe* de Molière au format XML/TEI : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&ref=l0012")
}}

Les **fragments** entre le **fragment** dont la **référence** est *a1-s1_05* (niveau 3) et le **fragment** dont la **référence** est *l0023* (niveau 4) au format XML/TEI : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1-s1_05&end=l0023")
}}

### Options DoTS

Tous les **fragments** du **document** *Le Tartuffe* de Molière pour lesquels le tour de parole est Tartuffe : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&filter=tei:role=Tartuffe")
}}

Tous les **fragments** entre l'acte 1 et l'acte 3 du **document** *Le Tartuffe* de Molière dont le tour de parole est celui de *Orgon*, au format HTML : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1&end=a3&filter=tei:role=Orgon&mediaType=html")
}}

Le **fragment** dont la référence est *a4* (acte 4) du **document** *Le Tartuffe* de Molière, en excluant les **fragments "enfants"** : 

{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&ref=a4&excludeFragments=true")
}}
