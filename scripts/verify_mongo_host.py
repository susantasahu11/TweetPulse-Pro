import os
import sys
from pymongo import MongoClient

DEFAULT_URI = "mongodb://127.0.0.1:27018/?directConnection=true"

def main():
    uri = os.environ.get("MONGO_URI") or (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URI)
    print(f"Using URI: {uri}")
    c = MongoClient(uri)
    dbs = [d['name'] for d in c.list_databases()]
    print("databases:", dbs)
    if 'bigdata_project' in dbs:
        cols = c['bigdata_project'].list_collection_names()
        print("bigdata_project collections:", cols)
    else:
        print("bigdata_project not found")

if __name__ == "__main__":
    main()
