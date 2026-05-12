#!/bin/bash

docker exec kafka kafka-topics \
  --create \
  --if-not-exists \
  --topic hospital-events \
  --bootstrap-server 127.0.0.1:9092 \
  --partitions 1 \
  --replication-factor 1

docker exec kafka kafka-topics \
  --create \
  --if-not-exists \
  --topic hospital-predictions \
  --bootstrap-server 127.0.0.1:9092 \
  --partitions 1 \
  --replication-factor 1

docker exec kafka kafka-topics \
  --list \
  --bootstrap-server 127.0.0.1:9092