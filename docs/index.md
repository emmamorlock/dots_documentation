# DoTS

## Qu’est-ce que c’est quoi ?

Implémentation method GET de DTS.

## Installation

**1. BaseX**

Télécharger BaseX (>= 10.0): [https://basex.org/download/](https://basex.org/download/)

- Privilégier le `ZIP Package`
- Pré-requis : [https://docs.basex.org/wiki/Startup#Startup](https://docs.basex.org/wiki/Startup#Startup)


**2. DoTS**


```Bash
cd path/to/basex/webapp
```

``` {.Bash .copy}
git clone https://github.com/chartes/dots.git
```

La structure de votre instance BaseX doit être la suivante :


	basex/				# BaseX root dir.
		bin/			# Start scripts (GUI, HTTP server, etc.).
		data/			# The database directory.
		webapp/			# Web Application directory.
			dots/		# DoTS module (DTS reslover, etc.).
		...				# Other.



La structure de `webapp/dots` est la suivante :

	dots/
		api/			# Resolver lib.
		lib/			# Projects db management tools.
		schema/			# Dots resources validation schemas.
		scripts/		# Projects db management cmd.
		globals.xqm		# Dots resources default paths.
		README.md

