from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.telegram import text_to_docs
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values

from vector_database import Vector_Database
from indexing import Indexer

class HyDE:
    def __init__(self) -> None:
        self.config = dotenv_values(".env")
        self.hyde_prompt = "Write a detailed article based on your prior knowledge about: {question}"

    def generate_document(self, user_prompt):
            hyde_prompt_template = ChatPromptTemplate.from_template(self.hyde_prompt)
            llm=ChatOpenAI(
                model="gpt-4.1-mini",
                api_key=self.config["OPENAI_API_KEY"]
            )

            doc_generation_chain = (
                hyde_prompt_template
                | llm
                | StrOutputParser()
                | text_to_docs
            )

            document = doc_generation_chain.invoke(
                 {"question": user_prompt}
            )

            return document
        

    def get_relevant_chunks(self, user_prompt):
        document = self.generate_document(user_prompt)
        # hyde_prompt_template = ChatPromptTemplate.from_template(self.hyde_prompt)
        
        # Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )

        indexer = Indexer(document=document, text_splitter=text_splitter)
        docs = indexer.chunking()
        
        # Embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", 
            # api_key=dotenv_values(".env.OPENAI_API_KEY"),
            api_key=self.config["OPENAI_API_KEY"],
        )

        # Storing data in Vector Store
        db_collection_name="query_translations"
        vector_db = Vector_Database(
            database_client=QdrantClient,
            database_vector_store=QdrantVectorStore,
            database_url=self.config["QDRANT_CLOUD_CLUSTER_URL"],
            database_api_key=self.config["QDRANT_API_KEY"],
        )

        vector_db.delete_collection(db_collection_name)
        vector_store = vector_db.upload(
            docs=docs,
            embeddings=embeddings,
            db_grpc=True,
            db_collection_name=db_collection_name
        )

        relevant_chunks = vector_store.similarity_search(user_prompt)

        return relevant_chunks


