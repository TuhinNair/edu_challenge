FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY . /src/
RUN ./bin/build.sh
ENTRYPOINT ["pipenv", "run"]