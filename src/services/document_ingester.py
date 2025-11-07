from docling.document_converter import DocumentConverter
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
import os
import requests
from services.vector_store_manager import VectorStoreManager

# Load environment variables from .env file
load_dotenv()

# contains logic for querying mongo for config file, parsing pdf to markdown and retrieving it to ingest to vector db 
class DocumentIngester:
    def __init__(self):
        self.connection_string = "http://host.docker.internal:3000/v1/api/bucketconfig"
        self.vector_store_manager = VectorStoreManager()
    
    def _get_folder_path_from_file(self, file_path):
        file_dir = os.path.dirname(file_path)
        folder_path_for_query = os.path.basename(file_dir) if file_dir else "wild_animals"  # Extract "wild_animals" from path
        return folder_path_for_query
    
    def _fetch_config(self, folder_path_for_query):
        try:
            response = requests.get(f"{self.connection_string}/{folder_path_for_query}")

            if response.status_code != 200:
                print(f"API request failed with status code: {response.status_code}")
                exit(1)  # Exit with error code 1

            print(response)
            config = response.json()
            return config
        except Exception as e:
          print(f"Error fetching config from API: {e}")
          exit(1)  # Exit with error code 1
    
    def _extract_config_values(self, config):
        chunk_size = config.get('chunk_size')
        chunk_overlap = config.get('chunk_overlap')
        chunk_strategy = config.get('chunk_strategy')
        namespace = config.get('namespace')
        index_name = config.get('index_name')
        metadata_extraction = config.get("metadata_extraction")
        print(f"Using configs from API response: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, namespace={namespace}, index_name={index_name}")
        return chunk_size, chunk_overlap, chunk_strategy, namespace, index_name, metadata_extraction
    
    def _convert_pdf_to_markdown(self, file_path):
        # Parsing doc with Docling ****************************************************
        source = file_path # document per local path or URL
        converter = DocumentConverter()
        result = converter.convert(source)
        parsed_md = result.document.export_to_markdown() #  pdf to markdown 
        return parsed_md
    
    def _save_markdown_file(self, parsed_md, file_path, folder_path_for_query):
        filename_with_extension = os.path.basename(file_path)
        filename_without_extension = os.path.splitext(filename_with_extension)[0]
        md_file_path = f"../files/{folder_path_for_query}/{filename_without_extension}.md"

        # Code to create md file for parse file 
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(parsed_md )
        
        return md_file_path
    
    def _load_documents(self, md_file_path):
        # Load the parse.md file
        file_md = SimpleDirectoryReader(input_files=[md_file_path]).load_data()
        return file_md
    
    def process_document(self, file_path):
        folder_path_for_query = self._get_folder_path_from_file(file_path)
        
        config = self._fetch_config(folder_path_for_query)
        chunk_size, chunk_overlap, chunk_strategy, namespace, index_name, metadata_extraction = self._extract_config_values(config)
       
        parsed_md = self._convert_pdf_to_markdown(file_path)
        md_file_path = self._save_markdown_file(parsed_md, file_path, folder_path_for_query)
        file_md = self._load_documents(md_file_path)

        # Use VectorStoreManager to handle database operations
        self.vector_store_manager.ingest_documents(
            documents=file_md,
            index_name=index_name,
            namespace=namespace,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

