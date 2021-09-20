#!/bin/bash

mkdir build
mkdir build/data
mkdir build/models
echo "Downloading Glove embeddings"
curl "https://nlp.stanford.edu/data/glove.twitter.27B.zip" -o build/data/glove_embeddings.zip
curl "https://emtract.s3.us-west-2.amazonaws.com/models/twitter.h5" -o build/models/twiter.h5