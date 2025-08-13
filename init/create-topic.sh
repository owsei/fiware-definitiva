#!/bin/bash
set -e

BROKER="kafka:9092"
TOPIC="iot_data"

echo "⏳ Esperando a que Kafka esté disponible en $BROKER..."

# Esperar hasta que Kafka responda
RETRIES=20
for i in $(seq 1 $RETRIES); do
    if kafka-topics.sh --bootstrap-server $BROKER --list > /dev/null 2>&1; then
        echo "✅ Kafka está disponible"
        break
    fi
    echo "⚠️  Kafka no está listo, reintentando ($i/$RETRIES)..."
    sleep 3
done

# Crear el topic si no existe
echo "📌 Creando topic '$TOPIC'..."
kafka-topics.sh --create \
  --if-not-exists \
  --topic "$TOPIC" \
  --bootstrap-server "$BROKER" \
  --partitions 1 \
  --replication-factor 1
echo "✅ Topic '$TOPIC' listo"
