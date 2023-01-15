### mongo
from pymongo import MongoClient

client = MongoClient(host = 'localhost', port = 27017, username = "root", password = "example")
with client:
    db = client["ftp_data"]

    cars = [ {'name': 'Audi', 'price': 52642},
        {'name': 'Mercedes', 'price': 57127},
        {'name': 'Skoda', 'price': 9000},
        {'name': 'Volvo', 'price': 29000},
        {'name': 'Bentley', 'price': 350000},
        {'name': 'Citroen', 'price': 21000},
        {'name': 'Hummer', 'price': 41400},
        {'name': 'Volkswagen', 'price': 21600} ]

    collection = db["cars"]
    collection.drop()
    collection.insert_many(cars)
    cursor = collection.find({})
    for i in cursor:
        print(i)
    print(db.list_collection_names())
### redis

import redis

r = redis.StrictRedis(host='localhost', port = 6379, db = "1")
r.set('ip_address', '127.0.0.0')
print(r.get('ip_address'))






