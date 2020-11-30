import faust

app = faust.App('example_faust_app',
                broker='kafka:9092',
                value_serializer='raw'
               )

# The @app.on_configured.connect (and @app.on_before_configured.connect)
# decorators tell faust to run functions as part of starting up the app.
# This is useful for code that we want to run before trying to connect
# to Kafka but not, e.g., if this file is imported by another file.
@app.on_configured.connect
def pre_configure(app, conf, **kwargs):
    app.message_max_length = 15
    print("Now we're configured!")

input_stream = app.topic('example_kafka_topic1')

@app.agent(input_stream)
async def report_messages_received(messages):
    async for message in messages:
        if len(message) > app.message_max_length:
            raise ValueError("Message length too long!")
        print(message)

if __name__ == '__main__':
    app.main()
