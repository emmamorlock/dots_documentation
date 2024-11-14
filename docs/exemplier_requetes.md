# "Exemplier" de requêtes d'API DTS

Vocabulaire

Un **projet** est une collection DTS de premier niveau.

## Le endpoint `Collection`

### Requêtes DTS compatibles

La liste des **projets** disponibles : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection")
}}

La liste des collections du **projet** *theater* et leurs métadonnées : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=theater")
}}

La liste des **documents** de la **collection** *Molière* et leurs métadonnées : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere")
}}

La liste des métadonnées du **document** *L'avare* de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_avare")
}}

La liste des collections auxquelles le **document** *Le Tartuffe* de Molière appartient : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere_tartuffe&nav=parents")
}}

### Requêtes DoTS

La liste des **documents** de la **collection** _Molière_ pour lesquels la métadonnée `dc:date` est _1669_ : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/collection?id=moliere&filter=dc:date=1669")
}}

## Le endpoint `Navigation`

### Requêtes "DTS compatibles"

La liste des **passages** de niveau 1 du **document** *Le Tartuffe* de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=1")
}}

La liste des **passages** de niveau 1 et 2 du **document** *Le Tartuffe* de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=2")
}}

La liste de tous les passages du **document** *Le Tartuffe* de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=-1")
}}

Les métadonnée du **passage** dont la **référence** est *a3* (acte 3) du **document** *Le Tartuffe* de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3")
}}

Les métadonnée du **passage** dont la **référence** est *a3* (acte 3) du **document** *Le Tartuffe* de Molière ainsi que la liste de tous les **passages** qu'il contient avec leurs métadonnées :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&ref=a3&down=-1")
}}

La liste des **passages** entre le **passage** dont la **référence** est *a3-s2* (acte 3, scène 2) et le **passage** dont la **référence** est *a3-s6* (acte 3, scène 6), et leurs métadonnées :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&start=a3-s2&end=a3-s6")
}}

La liste de tous les **passages** de type _act_ dans **l'arbre de citation** parmi tous les **passages** du **document** _Le Tartuffe_ de Molière :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&tree=act&down=-1")
}}


### Requêtes DoTS

Tous les **passages** de niveau 3 (les tours de parole) dont la métadonnée `tei:role` est *Tartuffe* :
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/navigation?resource=moliere_tartuffe&down=3&filter=tei:role=Tartuffe")
}}

## Le endpoint `Document`

### Requêtes "DTS compatibles"

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

Le **passage** dont la **référence** est *l0012* (niveau 4) du **document** *Le Tartuffe* de Molière au format XML/TEI : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&ref=l0012")
}}

Les **passages** entre le **passage** dont la **référence** est *a1-s1_05* (niveau 3) et le **passage** dont la **référence** est *l0023* (niveau 4) au format XML/TEI : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1-s1_05&end=l0023")
}}

### Requêtes DoTS

Tous les **passages** du **document** *Le Tartuffe* de Molière pour lesquels le tour de parole est Tartuffe : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&filter=tei:role=Tartuffe")
}}

Tous les **passages** entre l'acte 1 et l'acte 3 du **document** *Le Tartuffe* de Molière dont le tour de parole est celui de *Orgon*, au format HTML : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&start=a1&end=a3&filter=tei:role=Orgon&mediaType=html")
}}

Le **passage** dont la référence est *a4* (acte 4) du **document** *Le Tartuffe* de Molière, en excluant les **passages "enfants"** : 
{{ macro_collapse_card_api_doc(
  verb_http="get",
  url="https://dots.chartes.psl.eu/demo/api/dts/document?resource=moliere_tartuffe&ref=a4&excludeFragments=true")
}}
