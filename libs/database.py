from pymongo import MongoClient


class Database():
    
    def __init__(self, user: str, password: str, host: str,
                 database: str, collection: str):
        """ Connect to the MongoDB database """
        
        mongodb_url = f"mongodb+srv://{user}:{password}@{host}"
        mongodb_url += "/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(mongodb_url)
        self.db = self.client[database]
        self.collection = self.db[collection]
    
    def insert_data(self, rows: list[dict]) -> list:
        """ Insert data rows into the collection

        Args:
            rows (list[dict]): List of dictionaries containing the data to insert
            
        Returns:
            list: List of the inserted ids
        """
        
        result = self.collection.insert_many(rows)
        return result.inserted_ids
    
    def delete_collection(self):
        """ Delete full data of the collection """
        
        self.collection.delete_many({})