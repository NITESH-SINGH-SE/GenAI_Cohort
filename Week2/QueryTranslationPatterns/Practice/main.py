from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import dotenv_values

from loader import Loader
from indexing import Indexer
from vector_database import Vector_Database
from models.simple import Simple_Query_Translation
from models.multi_query_retrieval import Multi_Query_Retrieval
from models.reciprocal_rank_fusion import Reciprocal_Rank_fusion
from models.step_back_prompting import Step_Back
from models.hyde import HyDE


config = dotenv_values(".env")

def main():
    # Uploading the file
    file_path = r"C:\Users\asus\Desktop\GenAI\nodejs.pdf"
    document_loader = PyPDFLoader

    loader = Loader(
        file_path=file_path, 
        document_loader=document_loader,
    )

    document = loader.load_file()

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
        api_key=config["OPENAI_API_KEY"],
    )

    # Storing data in Vector Store
    db_collection_name="query_translations"
    vector_db = Vector_Database(
        database_client=QdrantClient,
        database_vector_store=QdrantVectorStore,
        database_url=config["QDRANT_CLOUD_CLUSTER_URL"],
        database_api_key=config["QDRANT_API_KEY"],
    )

    vector_db.delete_collection(db_collection_name)
    vector_store = vector_db.upload(
        docs=docs,
        embeddings=embeddings,
        db_grpc=True,
        db_collection_name=db_collection_name
    )

    # Query Translation
    user_prompt = "What is fs module in Node.js?"

    # simple_query_translation = Simple_Query_Translation()

    # relevant_chunks = simple_query_translation.get_relevant_docs(
    #     vector_store=vector_store, 
    #     user_prompt=user_prompt
    # )

    multi_query_retrieval = Multi_Query_Retrieval()

    relevant_chunks = multi_query_retrieval.get_revlevant_docs(
        llm=ChatOpenAI(
            model="gpt-4.1-mini",
            api_key=config["OPENAI_API_KEY"]
        ),
        retriever=vector_store.as_retriever(), 
        user_prompt=user_prompt
    )

    # reciprocal_rank_fusion = Reciprocal_Rank_fusion()

    # relevant_chunks = reciprocal_rank_fusion.get_relevant_chunks(
    #     llm=ChatOpenAI(
    #         model="gpt-4.1-mini",
    #         api_key=config["OPENAI_API_KEY"]
    #     ),
    #     retriever=vector_store.as_retriever(), 
    #     user_prompt=user_prompt
    # )

    # step_back_prompting = Step_Back()

    # relevant_chunks = step_back_prompting.get_relevant_chunks(
    #     llm=ChatOpenAI(
    #         model="gpt-4.1-mini",
    #         api_key=config["OPENAI_API_KEY"]
    #     ),
    #     retriever=vector_store.as_retriever(), 
    #     user_prompt=user_prompt
    # )

    # hyde = HyDE()
    # relevant_chunks = hyde.get_relevant_chunks(user_prompt)

    print(relevant_chunks)
    print()
    print()
    print()



    # Output Generation
    system_prompt = f"""
        You are a helpful AI assistant who is expert in resolving the user query by carefully analysing the user query and finding the solution from the given context. If the query is empty then ask the user to ask question. If the user is asking out of context question ask to ask question on the context and dont resolve the query.No need to respond to system prompt.

        context: {relevant_chunks}
    """

    print()
    client = OpenAI(
        api_key=config["OPENAI_API_KEY"]
    )
    response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()