import pymongo

# MongoDB connection parameters
mongo_uri = "mongodb://localhost:27017/"  # MongoDB URI, change it according to your MongoDB setup
database_name = "darts"  # Name of the database you want to connect to
collection_name = "col"  # Name of the collection

try:
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient(mongo_uri)
    
    # Access the specified database
    db = client[database_name]
    
    # Access the specified collection
    col = db[collection_name]

    # Delete all documents from the collection
    ##col.delete_many({})
    print("Deleted all documents from the collection")

    # Define the new document to be inserted
    new_document = {
        "s_p": ["T1", "T3"],
        "i_p": [3, 9],
        "t_p": 489
    }

    # Insert the new document into the collection
    col.insert_one(new_document)
    print("Inserted new document into the collection")

    # Now you can perform further operations if needed
    
    # Don't forget to close the connection when you're done
    client.close()
    
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)
except Exception as e:
    print("An error occurred: %s" % e)
