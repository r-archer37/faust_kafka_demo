import faust

app = faust.App('example_faust_app',
                broker='kafka:9092',
                value_serializer='raw'
               )

input_stream1 = app.topic('example_kafka_topic')
input_stream2 = app.topic('example_kafka_topic2')
input_stream_1_and_2 = app.topic('example_kafka_topic', 
                                 'example_kafka_topic2')


@app.agent(input_stream1)
async def report_messages_received1(messages):
    async for message in messages:
        print('\n'.join([
            'This message is from topic1',
            message.decode()
        ]))

        
@app.agent(input_stream2)
async def report_messages_received2(messages):
    async for message in messages:
        print('\n'.join([
            'This message is from topic2',
            message.decode()
        ]))


@app.agent(input_stream_1_and_2)
async def report_messages_received_1_and_2(messages):
    async for message in messages:
        print('\n'.join([
            'This message is from topic1 or topic2',
            message.decode()
        ]))


if __name__ == '__main__':
    app.main()
