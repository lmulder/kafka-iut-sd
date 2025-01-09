# kafka-iut-sd

## Installation de Kafka
* Ouvrir un terminal depuis la console OpenShift
* Lancer la commande suivante :
```bash
helm install my-kafka oci://registry-1.docker.io/bitnamicharts/kafka
```
## Récupération du mot de passe pour le user1
oc get secret my-kafka-user-passwords --namespace loic-mulder-dev -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1
Modifier le contenu du mot de passe "changeme" dans le fichier kubernetes/client-properties.yaml

## Installation d'un client Kafka
```bash
cd kubernetes
oc apply -f client-properties.yaml
oc apply -f kafka-client.yaml
```

## Connexion au pod kafka-client
Depuis la console web :
Workloads -> Pods -> kafka-client-xxxxxxxx-yyyyyyy -> Terminal

Ou en ligne de commande:
```bash
oc rsh kafka-client-xxxxxxxx-yyyyyyy
```

## Test de production
Connecté au pod kafka-client
```bash
kafka-console-producer.sh \
            --producer.config /tmp/client.properties \
            --bootstrap-server my-kafka.loic-mulder-dev.svc.cluster.local:9092 \
            --topic my-first-topic
>
```

Pour envoyer un message, à l'invite de commande ">", il suffit de saisir du texte et qppyer sur Entrée. Pour quitter le producter, taper Ctrl+C

## Test de consommation
Connecté au pod kafka-client
```bash
kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server my-kafka.loic-mulder-dev.svc.cluster.local:9092 \
            --topic my-first-topic \
            --from-beginning
```



