#!/bin/bash
echo "\n#################################################################################\n"
echo "Pre Check Cleanup for trashes"
echo "\n#################################################################################\n"
docker-compose down --rmi all
sudo docker system prune --volumes
sudo docker system prune

echo -e "\n#################################################################################\n"
echo "Starting Docker deployment for MQTT , KAFFA and Mongo DB"
echo "\n#################################################################################\n"
docker-compose up --build -d
echo -e "\n#################################################################################\n"
echo " Docker Deployment for  MQTT , KAFFA and Mongo DB successful"
echo "\n#################################################################################\n"
sleep 2m 30s

echo -e "\n#################################################################################\n"
echo "Cleanup Connectors Trash"
echo "\n#################################################################################\n"
curl -X DELETE http://localhost:8083/connectors/mqtt-source
curl -X DELETE http://localhost:8083/connectors/mongodb-sink

echo -e "\n#################################################################################\n"
echo "Starting MQTT Source Connector and MongoDB Sink Connector"
echo "\n#################################################################################\n"
curl -d @connect-mqtt-source.json -H "Content-Type: application/json" -X POST http://localhost:8083/connectors
curl -d @connect-mongodb-sink.json -H "Content-Type: application/json" -X POST http://localhost:8083/connectors
echo -e "\n#################################################################################\n"
echo  " Cloud Server is UP and Running"
echo -e "\n#################################################################################\n"
