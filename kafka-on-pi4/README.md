# Procédure pour Raspberry Pi 4 OS Lite (x64)

## Prérequis
- Raspberry OS Lite en version 64bits installé
- Paramétrage réseau (ethernet ou wifi) fait
- l'IP du rasberry sera noté {RPI_IP} dans la suite de la procédure (commande "ip a" pour obtenir l'IP de la carte ethernet "eth0" ou wifi "wlan0")

## Procédure d'installation de Kafka
1. Passage en root
sudo -s

2. Update
apt update

3. Installation de Java
sudo apt install default-jdk wget

4. Téléchargement de la dernière version de Kafka
cd /root
wget https://dlcdn.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz

5. Extraction de l'archive
mkdir /opt
cd /opt
tar -xzf /root/kafka_2.13-3.9.0.tgz
mv kafka_2.13-3.9.0 kafka
cd kafka

6. Paramétrage de kafka
nano config/kraft/server.properties
Modifier la ligne 
advertised.listeners=PLAINTEXT://{RPI_IP}:9092,CONTROLLER://{RPI_IP}:9093

7. Initialisation du stockage
export KAFKA_CLUSTER_ID=$($KAFKA_HOME/bin/kafka-storage.sh random-uuid)
./bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

8. Démarrage de Kafka
bin/kafka-server-start.sh config/kraft/reconfigure-server.properties

9. Arrêt de Kafka (pour paramétrer le démarrage automatique)
Ctrl+C

## Démarrage automatique de kafka
> cp kafka.service /etc/systemd/system
> systemctl daemon-reload
> systemctl enable kafka
> systemctl start kafka 
 

## Procédure d'installation de Kafka-UI
1. Installation de docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
2 . Installation de kafka-ui
mkdir /opt/kui
touch /opt/kui/config.yml
chmod 777 /opt/kui/config.yml
docker run -it -p 8080:8080 -e DYNAMIC_CONFIG_ENABLED=true --name kafka-ui -d -v /opt/kui/config.yml:/etc/kafkaui/dynamic_config.yaml

Pour arrêter le conteneur
> docker stop kafka-ui

Pour lancer le conteneur
> docker start kafka-ui

La configuration se fait directement depuis l'interface en rajoutant l'IP du serveur Kafka {RPI_IP} dans la liste des borkers.

En cas d'erreur au démarrage relative à la librairie commons-logging, il faut supprimer le conteneur et relancer
docker rm kafka-ui
docker run -it -p 8080:8080 -e DYNAMIC_CONFIG_ENABLED=true --name kafka-ui -d -v /opt/kui/config.yml:/etc/kafkaui/dynamic_config.yaml