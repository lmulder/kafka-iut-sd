# kafka-iut-sd

## Pré-requis
* Création d'un compte Red Hat Developers depuis developers.redhat.com
* Accès à la Developer Sandbox OpenShift. Le namespace utilisateur créé sera noté {user-namespace-dev}
* Télécharger les outils ligne de commande "oc" et "helm" depuis le menu Aide de la console OpenShift
* Dézipper et placer les .exe dans le dossier Downloads

## Installation de Kafka
* Ouvrir le Terminal Windows, se placer dans le répertoire Downloads
* Récupérer la commande de connexion depuis le menu profil de la console OpenShift
* Lancer la commande suivante :
```bash
oc login .......
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-kafka bitnami/kafka --set image.repository=bitnamilegacy/kafka
```
## Récupération du mot de passe pour le user1
```bash
oc get secret my-kafka-user-passwords --namespace {user-namespace-dev} -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1
Modifier le contenu du mot de passe "changeme" dans le fichier kubernetes/client-properties.yaml
```

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
            --bootstrap-server my-kafka.{user-namespace-dev}.svc.cluster.local:9092 \
            --topic my-first-topic
>
```

Pour envoyer un message, à l'invite de commande ">", il suffit de saisir du texte et qppyer sur Entrée. Pour quitter le producter, taper Ctrl+C

## Test de consommation
Connecté au pod kafka-client
```bash
kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server my-kafka.{user-namespace-dev}.svc.cluster.local:9092 \
            --topic my-first-topic \
            --from-beginning
```



