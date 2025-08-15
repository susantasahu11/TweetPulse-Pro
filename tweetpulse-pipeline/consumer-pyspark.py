# TweetPulse Pro - Kafka Spark Consumer
# Author: Manula Fernando
# Updated: July 23, 2025
# Description: Consumes tweets from Kafka, processes with Spark, stores results in MongoDB. Configurable via YAML and CLI.

import findspark
findspark.init()

import argparse
import logging
import sys
import yaml
import re
import nltk
import os
from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def clean_text(text):
    if text:
        text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
        text = re.sub(r'(@|#)\w+', '', text)
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ''

def main():
    parser = argparse.ArgumentParser(description='Kafka Spark Consumer')
    parser.add_argument('--config', default='consumer_config.yaml', help='Path to config YAML file')
    parser.add_argument('--topic', help='Kafka topic to consume (overrides config)')
    args = parser.parse_args()

    # Logging setup
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Load configuration
    config = load_config(args.config)
    topic = args.topic or config.get('kafka_topic', 'numtest')
    bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', config.get('kafka_bootstrap_servers', 'localhost:9092'))
    group_id = config.get('kafka_group_id', 'my-group')
    mongodb_host = os.environ.get('MONGODB_HOST', config.get('mongodb_host', 'localhost'))
    mongodb_port = int(os.environ.get('MONGODB_PORT', config.get('mongodb_port', 27017)))
    mongodb_db = config.get('mongodb_db', 'bigdata_project')
    mongodb_collection = config.get('mongodb_collection', 'tweets')
    model_path = config.get('model_path', 'logistic_regression_model.pkl')

    # Download nltk data silently
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    # Setup MongoDB client and collection
    client = MongoClient(mongodb_host, mongodb_port)
    db = client[mongodb_db]
    collection = db[mongodb_collection]

    # Initialize Spark Session and load ML pipeline model
    spark = SparkSession.builder.appName("classify tweets").getOrCreate()
    pipeline = PipelineModel.load(model_path)

    # Mapping predicted label indices to names
    class_index_mapping = {0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant"}

    # Create Kafka consumer
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[bootstrap_servers],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
    except Exception as e:
        logging.error(f"Failed to create KafkaConsumer: {e}")
        sys.exit(1)

    logging.info(f"Consuming from topic '{topic}'...")
    processed, errors = 0, 0

    for message in consumer:
        try:
            # Assume message.value is a dict with a 'text' key
            if isinstance(message.value, dict):
                tweet = message.value.get('text', '')
            else:
                tweet = str(message.value)

            preprocessed_tweet = clean_text(tweet)

            # Create Spark DataFrame for prediction
            data_df = spark.createDataFrame([(preprocessed_tweet,)], ["Text"])

            # Transform input using pipeline model and get prediction
            prediction_df = pipeline.transform(data_df)
            prediction = prediction_df.collect()[0][6]  # Adjust index if needed depending on your pipeline output

            sentiment_label = class_index_mapping.get(int(prediction), "Unknown")

            logging.info(f"Tweet: {tweet}")
            logging.info(f"Predicted Sentiment: {prediction} ({sentiment_label})")

            # Insert into MongoDB
            tweet_doc = {
                "tweet": tweet,
                "prediction": sentiment_label
            }
            collection.insert_one(tweet_doc)

            processed += 1

        except Exception as e:
            logging.error(f"Error processing message: {e}")
            errors += 1

        if processed > 0 and processed % 100 == 0:
            logging.info(f"Processed {processed} tweets, {errors} errors so far.")

if __name__ == '__main__':
    main()
