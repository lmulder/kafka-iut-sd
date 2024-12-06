# kafka-iut-sd

## Installation de Kafka
* Ouvrir un terminal depuis la console OpenShift
* Lancer la commande suivante :
```bash
helm install kafka oci://registry-1.docker.io/bitnamicharts/kafka
```

## Installation d'un client Kafka
```bash
cd kubernetes
oc apply -f client-properties.yaml
oc apply -f kafka-client.yaml# kafka-iut-sd
oc get pods
