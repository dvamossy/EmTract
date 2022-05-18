#!/bin/bash

pip3 install -r requirements.txt

mkdir build
mkdir build/models
mkdir build/models/emotion-twitter
mkdir build/models/emotion-stocktwits

echo "Downloading Models"
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/added_tokens.json" -o build/models/emotion-twitter/added_tokens.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/config.json" -o build/models/emotion-twitter/config.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/special_tokens_map.json" -o build/models/emotion-twitter/special_tokens_map.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/tokenizer.json" -o build/models/emotion-twitter/tokenizer.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/tokenizer_config.json" -o build/models/emotion-twitter/tokenizer_config.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/vocab.txt" -o build/models/emotion-twitter/vocab.txt
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-twitter/pytorch_model.bin" -o build/models/emotion-twitter/pytorch_model.bin
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/added_tokens.json" -o build/models/emotion-stocktwits/added_tokens.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/config.json" -o build/models/emotion-stocktwits/config.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/special_tokens_map.json" -o build/models/emotion-stocktwits/special_tokens_map.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/tokenizer.json" -o build/models/emotion-stocktwits/tokenizer.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/tokenizer_config.json" -o build/models/emotion-stocktwits/tokenizer_config.json
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/vocab.txt" -o build/models/emotion-stocktwits/vocab.txt
curl "https://emtract.s3.us-west-2.amazonaws.com/models/emotion-stocktwits/pytorch_model.bin" -o build/models/emotion-stocktwits/pytorch_model.bin