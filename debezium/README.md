# Tutoriel Debezium

## Introduction

Ce tutoriel est une version adaptée du tutoriel officiel disponibile à l'url suivante : https://debezium.io/documentation/reference/stable/tutorial.html

Il en est une version simplifiée, les explications se trouvent sur le site officiel. Il s'agt ici des instructions minimalistes pour déployer une instance debezium consommant une database MySql d'exemple.

Le cluster kafka "my-kafka" a été déployé au préalable, il convient d'adapter le mot de passe du user1 dans le fichier d-debezium.yaml avant import dans OpenShift.

Les commandes peuvent être lancées depuis un Terminal directement depuis un Workspace Dev Spaces.

## Déploiement d'une source de données : MySQL
```
oc apply -f d-mysql.yaml
oc apply -f s-mysql.yaml
oc rsh mysql-xxxxxxx-yy
sh-4.4$  mysql -udebezium -pdbz
mysql> use inventory;
mysql> show tables;
mysql> select * from tables;
mysql> exit
sh-4.4$ exit
```

## Déploiement d'une instance de Debezium
```
oc apply -f d-debezium.yaml
oc apply -f s-debezium.yaml
# attente du démarrage du pod...
curl -H "Accept:application/json" http://debezium:8083
{"version":"4.1.1","commit":"be816b82d25370ce","kafka_cluster_id":"W5PAUBuQ6JtWI3yCyR2bCJ"}
curl -H "Accept:application/json" http://debezium:8083/connectors
[]
```

Aucun connector n'est déployé, c'est normal

## Déploiement du connecteur MySql paramétré pour se connecter à l'instance MySQL avec le user "debezium" à la databse "inventory" pour publier des events dans le topic "inventory" du cluster my-kafka
```
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" debezium:8083/connectors/ -d @inventory-connector.json
...
HTTP/1.1 201 Created
...
curl -H "Accept:application/json" http://debezium:8083/connectors
["inventory-connector"]
curl -i -X GET -H "Accept:application/json" http://debezium:8083/connectors/inventory-connector
...
```




