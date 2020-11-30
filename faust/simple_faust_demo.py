import faust

app = faust.App('example_faust_app',
                broker='kafka:9092',
                value_serializer='raw'
               )

input_stream = app.topic('example_kafka_topic1')

@app.agent(input_stream)
async def report_messages_received(messages):
    async for message in messages:
        print(message)

if __name__ == '__main__':
    app.main()
