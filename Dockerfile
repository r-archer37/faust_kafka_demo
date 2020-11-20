FROM jupyter/minimal-notebook:latest

RUN pip install --user faust pykafka

CMD ["jupyter", "lab"]