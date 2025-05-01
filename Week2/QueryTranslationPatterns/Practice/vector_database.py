class Vector_Database:
    def __init__(self, database_client, database_vector_store, database_url, database_api_key) -> None:
        self.database_client=database_client
        self.database_vector_store=database_vector_store
        self.database_url=database_url
        self.database_api_key=database_api_key
        self.client=None
        self.vector_store=None
        self.create_client()

    def create_client(self):
        self.client = self.database_client(
            url=self.database_url,
            api_key=self.database_api_key,
        )

    def delete_collection(self, collection_name):
        self.client.delete_collection(collection_name=collection_name)

    # def create_collection(self, collection_name):
    #     self.vector_store = self.database_vector_store.from_documents(
    #         docs = [],
    #         embeddings,
    #         url,

    #     )
        
    def upload(self, docs, embeddings, db_grpc, db_collection_name): 
        self.vector_store = self.database_vector_store.from_documents(
            documents = docs,
            embedding = embeddings,
            url=self.database_url,
            prefer_grpc=db_grpc,
            api_key=self.database_api_key,
            collection_name=db_collection_name,
        )

        return self.vector_store