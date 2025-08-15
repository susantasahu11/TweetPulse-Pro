
# TweetPulse Pro - Kafka Tweet Producer
# Author: Manula Fernando
# Updated: July 23, 2025
# Description: Reads tweets from CSV and streams to Kafka topic. Configurable via YAML and CLI.

import argparse
import csv
import json
import logging
import sys
import yaml
import os
from time import sleep
from kafka import KafkaProducer

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Kafka Tweet Producer')
    parser.add_argument('--config', default='producer_config.yaml', help='Path to config YAML file')
    parser.add_argument('--topic', help='Kafka topic to send to (overrides config)')
    parser.add_argument('--csv', help='CSV file to read tweets from (overrides config)')
    args = parser.parse_args()

    # Logging setup
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Load config
    config = load_config(args.config)
    topic = args.topic or config.get('topic', 'numtest')
    csv_file = args.csv or config.get('csv_file', 'twitter_validation.csv')
    bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', config.get('bootstrap_servers', 'localhost:9092'))
    csv_file = os.environ.get('CSV_FILE', csv_file)
    sleep_seconds = float(os.environ.get('SLEEP_SECONDS', config.get('sleep_seconds', 0.5)))

    logging.info(f"Starting producer for topic '{topic}' using file '{csv_file}' (bootstrap_servers={bootstrap_servers})")
    # Retry creating producer until Kafka becomes ready
    producer = None
    for attempt in range(1, 61):  # up to ~1 minute
        try:
            producer = KafkaProducer(
                bootstrap_servers=[bootstrap_servers],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            break
        except Exception as e:
            logging.warning(f"Kafka not ready (attempt {attempt}): {e}")
            sleep(1)
    if not producer:
        logging.error("Failed to create KafkaProducer after multiple attempts.")
        sys.exit(1)

    try:
        with open(csv_file, encoding='utf-8') as file_obj:
            reader_obj = csv.reader(file_obj)
            for idx, data in enumerate(reader_obj, 1):
                try:
                    producer.send(topic, value=data)
                    logging.info(f"Sent row {idx} to topic '{topic}': {data}")
                except Exception as send_err:
                    logging.error(f"Failed to send row {idx}: {send_err}")
                sleep(sleep_seconds)
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_file}")
    except Exception as e:
        logging.error(f"Error reading CSV or sending messages: {e}")

    producer.flush()
    logging.info("Producer finished sending all messages.")

if __name__ == '__main__':
    main()
    