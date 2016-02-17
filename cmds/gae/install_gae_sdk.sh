#!/bin/bash -xe

if [ ! -f .gen/google_appengine/appcfg.py ]; then

    rm -rf .gen/google_appengine .gen/gae.zip || true
    mkdir .gen || true

    wget "https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.32.zip" -O ".gen/gae.zip"
    cd .gen
    unzip gae.zip
    cd -

fi
