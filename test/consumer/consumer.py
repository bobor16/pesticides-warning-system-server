from kafka import KafkaConsumer
consumer = KafkaConsumer('foo', bootstrap_servers=['namenode:9092'], group_id='group1')

for msg in consumer:
    print (msg)