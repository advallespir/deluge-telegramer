#!/usr/bin/env bash

docker build --no-cache -t telegramer.build . \
    && docker run -v $(pwd)/out:/tmp/out --rm -i telegramer.build sh -s << COMMANDS
pip install --no-cache-dir build
python setup.py bdist_egg && python -m build
chown -R $(id -u):$(id -g) dist
cp -ar dist/ /tmp/out/
COMMANDS
