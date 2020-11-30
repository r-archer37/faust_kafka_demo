## Faust Demos
This directory has a few different demo faust apps that are designed to highlight different features.

### simple_faust_demo.py
The simplest demonstration: connect to kafka, print out the contents of messages. Hopefully this makes clear the basics, and that once the message is in memory, we are free to execute arbitrary code against it.

### two-topic_faust_demo.py
This file demonstrates that we can have multiple consumers listening to one topic, one consumer listening to multiple topics, and that they all process in parallel.

### config_faust_demo.py
Here we highlight how to configure a Faust app at the time of startup.

## Where Next?
Once you've played around with these three, why not take a look at a more complex demonstration of Faust's built-in Records and Tables features? https://faust.readthedocs.io/en/latest/playbooks/pageviews.html
