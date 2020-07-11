#!/bin/sh

pip install --upgrade pip && pip install pipenv

apk -q update && apk --no-cache add build-base && apk --no-cache add postgresql-dev

pipenv install --deploy 