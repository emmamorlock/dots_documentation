# Resolver

Lancer basexhttp: [https://docs.basex.org/wiki/Web_Application](bash basex -b dbName=encpos-c1 ../webapp/dots/scripts/dots_switcher_update.xq)

```sh
basex % bin/basexhttp
```

DoTS sert en premier lieu de résolveur pour l'API DTS [https://distributed-text-services.github.io/specifications/](https://distributed-text-services.github.io/specifications/).

DoTS offre un accès aux quatre endpoints de l'API DTS.

## Base API Endpoint

- Documentation : [https://distributed-text-services.github.io/specifications/Entry.html#base-api-endpoint](https://distributed-text-services.github.io/specifications/Entry.html#base-api-endpoint)
- Réponse d'API : consulter [http://localhost:8080/api/dts/](http://localhost:8080/api/dts/)

Cette réponse fournit les points d'entrée pour chacun des endpoints DTS. DoTS propose les URI suivantes :

- [http://localhost:8080/api/dts/collections](http://localhost:8080/api/dts/collections)
- [http://localhost:8080/api/dts/navigation](http://localhost:8080/api/dts/navigation)
- [http://localhost:8080/api/dts/document](http://localhost:8080/api/dts/document)


TODO: Swagger Doc

## Endpoint **Collection**

- Documentation : [https://distributed-text-services.github.io/specifications/Collection-Endpoint.html](https://distributed-text-services.github.io/specifications/Collection-Endpoint.html)

## Endpoint **Navigation**

- Documentation : [https://distributed-text-services.github.io/specifications/Navigation-Endpoint.html](https://distributed-text-services.github.io/specifications/Navigation-Endpoint.html)

## Endpoint **Document**

- Documentation : [https://distributed-text-services.github.io/specifications/Document-Endpoint.html](https://distributed-text-services.github.io/specifications/Document-Endpoint.html)