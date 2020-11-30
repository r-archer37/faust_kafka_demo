## Processing Streaming Data with Python

### Before we Begin
This article is the `readme.md` file of a github repository that contains all the code you'll need to try this out yourself. Download or clone it using the links above. The only software you'll need is [Docker Desktop](https://www.docker.com/products/docker-desktop), so go ahead get that too.

### Introduction & Motivation

Think about code you've written to analyze data in python -- what was the first thing the code did? If it's anything like data analysis code I've written, it started with loading data into memory from a database, or from a file that looks like a database (i.e, has a row-and-column structure). It's an easy thing to do; python has very effective tools to load data structured that way (as do R and any number of other programming languages).

Underlying the effectiveness of those tools is that storing in one location in a row-and-column structure actually embeds a huge amount of information about the data: the number of observations, the grain of observations, and the available features of the observations are all implicit there. But what if we want to process data that arrives to us as it is generated? Data like tweets and financial transactions don't appear in the world in groups of 1,000, so we need not force ourselves to process them that way.

The solution I will demonstrate is Faust ([https://faust.readthedocs.io/en/latest/](https://faust.readthedocs.io/en/latest/)), a powerful tool for processing data streams using pure python. Faust is a python package (just `pip install faust`) that was open-sourced by Robinhood. The official documentation of the package is not lacking, but it can be hard to start using and understanding this kind of high-level stream-processing tool without an interactive demonstration. That's why Part 2 of this article is an interactive demonstration that requires only this purpose-built Github repo and Docker desktop to follow along with.

### Part 0: What is Streaming Data?

Let's start by being more concrete about what we mean by "a stream." Within this article, I am going to talk about streams that look like an Apache Kafka topic, but from the perspective of the code we'll be writing, it's not all that different from, say, the public Twitter API or any number of other streams out there. Fundamentally, they are a queue to which messages (typically JSON blobs) can be published, and from which they can be consumed. The expected usage has a consumer subscribing to a topic, and then taking one messsage at a time off the end of the queue. The consumer will usually perform some sort of operation on the content of the message, and then come back for the next one.

For example, a Kafka instance might have topics like `incoming_payment_received` and `incoming_payment_processed`. When our software platform initially receives payment it might publish a message to the former, prompting a consumer to create a record in a payment database. Subsequently, when we have properly attributed that payment for accounting purposes, our application might publish a message to the latter topic, prompting a different consumer to update the corresponding record.

A key feature of these streams is that a consumer can finish processing all messages in the queue, and be in a state of waiting for the next one to arrive, either up to some time-limit set by a developer, or indefinitely.

### Part 1: Building a Faust App

For the purpose of this demonstration, let's assume we want to develop a process that will wait indefinitely for new messages, so long as the queue it is connected to exists. This is what Faust will call our `app`. The typical Faust app will have `agent`s, `topic`s, and connections between the them. Let's start by looking at a very simple app and then break down what's going on:

#### `my_example_faust_app.py`
```python
import faust

app = faust.App('example_faust_app',
                broker='kafka:9092',
                value_serializer='raw'
               )

input_stream = app.topic('example_kafka_topic')

@app.agent(input_stream)
async def report_messages_received(messages):
    async for message in messages:
        print(message)

if __name__ == '__main__':
    app.main()
```

Starting from the bottom of the code, the first block we see looks similar to how a lot of python code ends, by telling the program what to do when we simply execute this python file. The only difference is that we take advantage of Faust's App class' `main()` function instead of writing our own. This is great: we don't need to spend our time initializing logging or or sorting out the nitty-gritty of connecting to Kafka. Faust handles all of that for us.

```python
@app.agent(input_stream)
async def report_messages_received(messages):
    async for message in messages:
        print(message)
```

In this block everything after `for` is trivial, so let's instead focus on the top two lines which contain more exotic syntax. `async` tells us that this is a python loop/function that can be executed in parallel with other async python. The details of this are beyond the scope of this article (see: [asyncio](https://docs.python.org/3/library/asyncio.html)), but our program can to listen to many topics at once, so processing messages in parallel can be handy. The function name and input variable are arbitrary names. The decorator on the function `@app.agent(input_stream)` means that this function will be an instance of `faust.Agent` on the app topic we called `input_stream`. That is, messages coming from that stream will be routed to this function, letting us iterate over an indefinite series of messages.

```python
input_stream = app.topic('example_kafka_topic')
```

This line defines our input stream, an instance of `faust.Topic`. By default, if the string is the name of a topic that exists in the Kafka server we connect to, our app will set up to consume from that topic; if the topic doesn't exist, our app will create it, and then set up to consume from it. Recall that consuming from a stream like this simply means taking one message at a time from a queue, doing whatever we've programmed our app to do, and then repeating.

```python
import faust

app = faust.App('example_faust_app',
                broker='kafka:9092',
                value_serializer='raw'
               )
```

This block defines the core of our program; an instance of `faust.App`. We give it a name, `'example_faust_app'`, tell it what message broker it will be using (`'kafka:9092'` is a default address for Kafka connections), and optionally declare a message serializer (e.g., 'raw', 'json', for more on this see the official Faust docs). 

### Aside: Running a Faust app

There's one last piece of code now standing between us and executing our fast application. If we simply enter `python my_example_faust_app.py` into our terminal, we'll get a usage guide, rather than actually executing our program (recall that we're executing `faust.App.main`). In order to actually start our program, we need to start a Faust worker -- a concept that isn't critical to understand to write a simple program, but can enable scaling and redundancy required for critical production systems. To do that simply provide the keyword `worker` along with our terminal command: `python my_example_faust_app.py worker`. Now, so long as we're able to connect to Kafka at `kafka:9092`, we have a Faust app that will wait to process messages for as long as we let it.

### Part 2: Interactive Demonstration

For this demonstration, I make use of Jupyter Lab, Faust, Kafka, Zookeeper, and more. But in order to make setup reasonable, everything is packged up within Docker containers. In order to follow along, all you'll need is Docker Desktop and your terminal (though a git client is helpful). First up, download or clone this repository. Next, in a terminal, navigate to the root of the repository and run `docker-compose up`. This should generate a fair amount of text on your screen; in order to stop the process at any time you can use ctrl+c. If afterwards anything is lingering, you can fully remove it by executing `docker-compose down` in the same location.

Now, with the docker-compose still running, open a browser window and point it to `localhost:8888`. You should be prompted to enter a "Password or token" which is set to `faust`.

![enter "faust" as your token](/images/jupyter_lab_login.png)

Clicking Log In will bring you to the Jupyter Lab Launcher tab. From the Launcher, click Terminal. 

![click the terminal button to start a new terminal](/images/jupyter_lab_landing.png)

In the terminal, execute `python faust/simple_faust_demo.py worker`. First you should see an app readout, then, since this is your first time executing this program against this Kafka server, you'll see several errors come up. The application will resolve these on its own, and eventually you'll have a smiling face and a blinking cursor ready for you.

![the application will resolve these errors on its own](/images/faust_first_run.png)

Now, using the file browser on the left, open the `notebooks` folder, and then the `pykafka_producer.ipynb` notebook. We'll use this notebook to send messages to our Faust app via Kafka. We use the `pykafka` package, rather than Faust, because this allows a low-level interface that is great for an interactive demo, but would be much tougher to build an application around. In that notebook, execute the first three cells:

![executing the first three cells sends a messagae to kafka](/images/message_sent.png)

All of this is, of course, barely scratching the surface of what Faust can do. There are several more demonstrations in this repo to try out. And of course, much more is documented on the project's homepage: [https://faust.readthedocs.io](https://faust.readthedocs.io).

Thank you for reading!
