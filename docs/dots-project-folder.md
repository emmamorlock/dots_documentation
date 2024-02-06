# Le dossier de dépôt

Ce document présente les ressources utiles au bon chargement en base d’un dossier de projet.


## Déclarer la structure éditoriale du projet

La structuration du *dossier de dépôt* reflète la structure éditoriale du *projet*.

À l'intérieur du dossier `data/`, vous pouvez organiser vos documents en collections et sous-collections (ou laisser vos documents "à plat"). Le nom des fichiers est utilisé comme identifiant de la collection. Par défaut, le nom du dossier sert aussi de titre de collection. Il est recommander de déclarer dans un fichier TSV le titre des collections, et éventuellement toutes les métadonnées de votre choix.

Pour les documents, son titre et son identifiant sont par défaut le nom du fichier (sans `.xml`). Si le document TEI dispose d'un attribut `@xml:id` sur l'élément racine `TEI`, c'est cet attribut qui est utilisé comme identifiant.



## Déclarer les métadonnées des ressources du projet


Un exemple est disponible dans le data_test mis à disposition avec cette documentation: [https://github.com/chartes/dots_documentation/blob/dev/data_test/periodiques/encpos_by_abstract/metadata/dots_metadata_mapping.xml](https://github.com/chartes/dots_documentation/blob/dev/data_test/periodiques/encpos_by_abstract/metadata/dots_metadata_mapping.xml).

Toutes les métadonnées à lier aux ressources doivent être déclarées dans le document XML `metadata/dots_metadata_mapping.xml`.

La déclaration d'une métadonnée se fait en ajoutant dans le document `metadata/dots_metadata_mapping.xml`, à l'intérieur de l'élément `<member/>`, un élément XML de son choix respectant quelques principes, selon les cas suivants :

### Métadonnée récurrente pour un type de ressource

Il peut être utile de déclarer une métadonnée dont le contenu ne diffère pas soit à l'échelle des collections soit à l'échelle des documents. DoTS offre ici la possibilité de déclarer simplement cette information.

**Modèle**
```xml
<propriété scope="collection|document" resourceId="all" value=".">Valeur de la métadonnée</propriété>
```
**Exemple**
```xml
<dc:licence scope="collection" resourceId="all" value=".">https://creativecommons.org/licenses/by/4.0/</dc:licence>
```
- `<propriété/>` : le nom de l'élément permet de définir la propriété attendue en réponse de la requête API. Dans l'exemple, la propriété est la licence en dublin core.
- `@scope` : la valeur attendue est *collection* ou *document*, selon la porté de la métadonnée.
- `@resourceID` : la valeur doit être ici *all* pour spécifier que la métadonnée concerne l'ensemble des ressources (collection ou document).
- le contenu de l'élément correspond à la valeur attendue pour la réponse d'API.

### Métadonnée issue d'un tableur TSV

**Modèle**
```xml
<propriété 
	scope="collection|document" 
	format="csv"
	source="/path/to/TSV"
	resourceId="id" 
	value="content"/>
```
**Exemple**
```xml
<dc:date 
	scope="collection" 
	format="csv"
	source="./documents_metadata.tsv"
	resourceId="id" 
	value="promotion_year"/>
```

Exemple de TSV

|id|promotion_year|
|--|--------------|
|ENCPOS_1849|1849|

- `<propriété/>` : le nom de l'élément permet de définir la propriété attendue en réponse de la requête API. Dans l'exemple, la propriété est la date en dublin core.
- `@scope` : la valeur attendue est *collection* ou *document*, selon la porté de la métadonnée.
- `@format` : la valeur attendue est *csv*.
- `@source` : permet d'indiquer le nom du fichier CSV. Le nom du fichier donné ici doit correspondre au nom du fichier correspondant déposé dans le dossier de dépôt dans `metadata/`.
- `@resourceId` : dans le CSV, l'identifiant de la collection (c'est à dire le nom du dossier correspondant) ou l'identifiant du document (c'est à dire l'attribut `@xml:id` de l'élément racine `TEI` ou à défaut le nom du fichier sans `.xml`) doit être renseigné. La valeur attendue dans ``@resourceId` est le nom de la colonne où se trouvent ces identifiants.
- `@value` : la valeur attendue ici est le nom de la colonne où se trouve la valeur de la métadonnée.

### Métadonnée inscrite dans la source XML/TEI

**Modèle**
```xml
<propriété 
	scope="document" 
	xpath="/path/to/metadata"/>
```
**Exemple**
```xml
<dc:title 
	scope="document" 
	xpath="//titleStmt/title[@type = 'main' or position() = 1]"/>
```
- `<propriété/>` : le nom de l'élément permet de définir la propriété attendue en réponse de la requête API. Dans l'exemple, la propriété est le titre en dublin core.
- `@scope` : la valeur attendue, dans ce cas, est *document*. DoTS ne permet pas de définir des métadonnées de collection qui viendrait d'un document XML.
- `@xpath` : l'évaluation par DoTS du xpath défini ici permet de renseigner la valeur de la métadonnée.

D'autres fonctionnalités sont par ailleurs disponibles dans tous les cas de figure.
Il est notamment possible de typer les métadonnées : l'attribut `@type` peut prendre la valeur *number* ou *boolean* selon les besoins.
**NB. Attention cependant: si la valeur ne correspond pas au type demandé, la réponse d'API affiche une erreur.**
Enfin, un mécanisme de préfixage et de suffixage est disponible pour compléter au besoin les métadonnées des TSV. Les attributs `@prefix` et `@suffix` peuvent être utilisés.
