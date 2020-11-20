from pykafka import KafkaClient, Topic
import pykafka

def get_topic(topic_name: str, client: KafkaClient) -> Topic:
    topic = client.topics[topic_name.encode()]
    
    assert topic_name.encode() in client.topics.keys()
    
    return topic

def produce_to_topic(topic: Topic, message: str) -> None:
    with topic.get_sync_producer() as producer:
        producer.produce(message.encode())
