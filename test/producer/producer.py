import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='namenode9092')
for _ in range(100):
    producer.send('foobar', b'some_message_bytes')
future = producer.send('foobar', b'another_message')
result = future.get(timeout=60)

producer.flush()

producer.send('foobar', key=b'foo', value=b'bar')

producer = KafkaProducer(
    value_serializer=lambda v: json.dump(v).encode('utf-8'))
producer.send('fizzbuzz', {'foo': 'bar'})

producer = KafkaProducer(key_serializer=str.encode)
producer.send('flipflap', key='ping', value=b'1234')

producer = KafkaProducer(compression_type='gzip')
for i in range(1000):
    producer.send('foobar', b'msg %d' % i)
