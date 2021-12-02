#!/bin/bash

pip3 install -r requirements.txt

mkdir build
mkdir build/models
echo "Downloading Models"
curl "https://emtract.s3.us-west-2.amazonaws.com/models/twitter.h5" -o build/models/twitter.h5
curl "https://emtract.s3.us-west-2.amazonaws.com/models/stocktwits.h5" -o build/models/stocktwits.h5

