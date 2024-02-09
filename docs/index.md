# DoTS

## What is DTS?

The Distributed Text Services (DTS) Specification defines an API for working with collections of text as machine-actionable data.

Publishers of digital text collections can use the DTS API to help them make their textual data Findable, Accessible, Interoperable and Reusable (FAIR).

[https://distributed-text-services.github.io/specifications](https://distributed-text-services.github.io/specifications)


## What is DoTS?

DoTS is a XQuery implementation of DTS using a [BaseX](https://basex.org/) backend.

!!! Note

    **DoTS supports only DTS GET requests** for browsing collections, document retrieval and navigation.

## Capabilities

Using DoTS, you can

- with the DTS Collections endpoint:
	- Retrieve lists of collection members.
	- Retrieve metadata about individual collection items.
- with the DTS Navigation endpoint:
	- Retrieve lists of citeable passages within a text.
	- Retrieve lists of citeable passages within a text as groups of client-defined sizes (e.g. groups of 10 lines).
	- Retrieve metadata about the citation structure of a document.
- with the DTS Document endpoint:
	- Retrieve a single text passage at any level of the citation hierarchy.
	- Retrieve a range of text passages with a clearly defined start and end passage.
	- Retrieve an entire text.

## Install

### BaseX

Download BaseX (>= 10.0): [https://basex.org/download/](https://basex.org/download/)

- Prefer `ZIP Package`
- Requirements : [https://docs.basex.org/wiki/Startup#Startup](https://docs.basex.org/wiki/Startup#Startup)


### DoTS


```Bash
cd path/to/basex/webapp
```

``` {.Bash .copy}
git clone https://github.com/chartes/dots.git
```

The structure of your BaseX should be as follows:


	basex/				# BaseX root dir.
		bin/			# Start scripts (GUI, HTTP server, etc.).
		data/			# The database directory.
		webapp/			# Web Application directory.
			dots/		# DoTS module (DTS reslover, etc.).
		...				# Other.


<!--
La structure de `webapp/dots` est la suivante :

	dots/
		api/			# Resolver lib.
		lib/			# Projects db management tools.
		schema/			# Dots resources validation schemas.
		scripts/		# Projects db management cmd.
		globals.xqm		# Dots resources default paths.
		README.md
-->

## Start DTS resolver

```Bash
cd path/to/basex/
bin/basexhttp
```

By default, the base DTS API enpoint is available at [http://localhost:8080/api/dts/](http://localhost:8080/api/dts/).