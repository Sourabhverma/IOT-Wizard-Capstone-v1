#!/bin/bash
echo "Pre Check Cleanup for trashes"
docker-compose down --rmi all
sudo docker system prune --volumes
sudo docker system prune


echo "Starting Docker deployment for MQTT , KAFFA and Mongo DB"
docker-compose up --build -d

echo " Docker Deployment for  MQTT , KAFFA and Mongo DB successful"
sleep 2m 30s

echo "Starting MQTT Source Connector and MongoDB Sink Connector"
curl -X DELETE http://localhost:8083/connectors/mqtt-source
curl -X DELETE http://localhost:8083/connectors/mongodb-sink
curl -d @connect-mqtt-source.json -H "Content-Type: application/json" -X POST http://localhost:8083/connectors
curl -d @connect-mongodb-sink.json -H "Content-Type: application/json" -X POST http://localhost:8083/connectors
