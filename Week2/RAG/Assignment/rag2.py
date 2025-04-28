from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

# Embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="my_documents",
    url="http://localhost:6333",
)

while True:
    query = input("> ")
    results = qdrant.similarity_search(query)

    client = OpenAI()

    system_prompt="""
        You are a helpful AI assitant. Generate response based on the following context

        context: {results}
    """

    completions = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print(completions.choices[0].message.content)