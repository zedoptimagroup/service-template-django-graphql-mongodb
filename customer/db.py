from pymongo import MongoClient

client = MongoClient("mongodb://microservice_demo_admin:NikolaTesla123@localhost:28888/microservice-demo-db?authSource=admin")
db = client["microservice-demo-db"]
customers_collection = db["customers"]