FROM continuumio/miniconda3
COPY env.yml .
COPY . /opt/flask-app/
SHELL [ "/bin/bash", "--login", "-c" ]

RUN conda env update --file env.yml --prune
RUN conda init bash
CMD ["flask", "run"]