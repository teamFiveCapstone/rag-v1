from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# logic to set up db connection and ingest documents 
class VectorStoreManager:
    def __init__(self):
        pass
    
    def _setup_pinecone_index(self, index_name):
        # Initialize connection to Pinecone
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

        # Get or create index (text-embedding-3-small has 1536 dimensions)
        # Create your index (can skip this step if your index already exists)
        try:
            pc.create_index(
                index_name,
                dimension=1536,  # text-embedding-3-small dimension
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        except Exception:
            # Index already exists, continue
            pass

        # Initialize your index
        pinecone_index = pc.Index(index_name)
        return pinecone_index
    
    def _create_vector_store(self, pinecone_index, namespace):
        # Initialize VectorStore with namespace
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index,
            namespace=namespace
        )
        return vector_store
    
    def _create_ingestion_pipeline(self, chunk_size, chunk_overlap, vector_store):
        # Create embedding model
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")

        # Create ingestion pipeline with transformations
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap),  # measure by tokens
                embed_model,
            ],
            vector_store=vector_store,
        )
        return pipeline
    
    def _ingest_documents(self, pipeline, file_md):
        # Ingest directly into vector db
        pipeline.run(documents=file_md)
    
    def ingest_documents(self, documents, index_name, namespace, chunk_size, chunk_overlap):
        pinecone_index = self._setup_pinecone_index(index_name)
        vector_store = self._create_vector_store(pinecone_index, namespace)
        pipeline = self._create_ingestion_pipeline(chunk_size, chunk_overlap, vector_store)
        self._ingest_documents(pipeline, documents)

