from kafka import KafkaProducer
import json
import time
import datetime
import random

KAFKA_BROKER = 'kafka:9092'
TOPIC = 'mi-topic'
TOPIC2 = 'iot_data'

# Esperar hasta que Kafka esté disponible
for i in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ Conectado a Kafka")
        break
    except Exception as e:
        print(f"⏳ Kafka no disponible, reintentando... ({i+1}/10)")
        time.sleep(3)
else:
    raise Exception("❌ No se pudo conectar a Kafka")

# Enviar mensajes continuamente
contador = 0
while True:
    mensaje = {
        "numero": contador,
        "texto": f"Mensaje {contador}",
        "timestamp": datetime.datetime.now().isoformat()
    }
    producer.send(TOPIC, mensaje)
    print(f"📤 Enviado: {mensaje}")
    
    mensaje2 = {
        "iot_id": 1,
        "temperature": random.randint(20, 40),
        "timestamp": datetime.datetime.now().isoformat()
    }
    producer.send(TOPIC2, mensaje2)
    print(f"📤 Enviado: {mensaje2}")
    
    contador += 1
    time.sleep(5)  # Espera entre mensajes


# No se cierra porque es un flujo continuo

while True:
   
    contador += 1
    time.sleep(5)  # Espera entre mensajes