from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

file_path=Path(__file__).parent.joinpath('nodejs.pdf')

# Loading the document
loader = PyPDFLoader(file_path)
docs = loader.load()

# Splitting the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)

# Embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 
qdrant = QdrantVectorStore.from_documents(
    documents=texts,
    embedding=embeddings,
    url='http://localhost:6333/',
    collection_name="my_documents",
)

