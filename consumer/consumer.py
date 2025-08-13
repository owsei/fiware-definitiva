from kafka import KafkaConsumer
import json
import time

KAFKA_BROKER = 'kafka:9092'

# Esperar hasta que Kafka esté disponible
for i in range(10):
    try:
        consumer = KafkaConsumer(
            'mi-topic',
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        break
    except Exception as e:
        print(f"⏳ Kafka no disponible, reintentando... ({i+1}/10)")
        time.sleep(3)
else:
    raise Exception("❌ No se pudo conectar a Kafka")

print("📥 Esperando mensajes...")
for mensaje in consumer:
    print(f"✅ Recibido: {mensaje.value}")
