from docling.document_converter import DocumentConverter
from chonkie import SentenceChunker
from pathlib import Path
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader
import json


# Parsing doc with Docling ****************************************************
source = "../files/lion.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)

lionPDF_md = result.document.export_to_markdown() #  pdf to markdown 

# code to create md file for output 
with open("../files/parsed_lion.md", "w", encoding="utf-8") as f:
    f.write(lionPDF_md )


# Chunking with Chonkie (sentence chunker )++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Basic initialization with default parameters

# chunker = SentenceChunker(
#     tokenizer="character",     # Default tokenizer (or use "gpt2", etc.)
#     chunk_size=800,           # Maximum tokens per chunk
#     chunk_overlap=50,         # Overlap between chunks
#     min_sentences_per_chunk=1  # Minimum sentences in each chunk
# )


# file_path = Path("/files/parsed_lion.md")
# text = file_path.read_text(encoding="utf-8")

# chunks = chunker.chunk(text)

# # Write chunks to markdown file
# with open("/files/chonkie_chunked_lion.md", "w", encoding="utf-8") as f:
#     chunk_lines = []
#     for index, chunk in enumerate(chunks, start=1):
#         chunk_text = chunk.text if hasattr(chunk, 'text') else str(chunk)
#         chunk_lines.append(f'## Chunk {index}\n\n{chunk_text}\n\n')
#     f.write(''.join(chunk_lines))


# Chunking with Lllamaindex (sentence splitter)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# # Load the lion.md file
# lionMD= SimpleDirectoryReader(input_files=["/files/parsed_lion.md"]).load_data()

# # measured by tokens
# splitter = SentenceSplitter(
#     chunk_size=400,
#     chunk_overlap=20,
# )
# nodes = splitter.get_nodes_from_documents(lionMD)



# # Write each node with only important properties to file
# with open("/files/llama_chunked_lion.md", "w", encoding="utf-8") as f:
#     for i, node in enumerate(nodes, 1):
#         f.write(f"\n{'='*80}\n")
#         f.write(f"NODE {i}\n")
#         f.write(f"{'='*80}\n")
        
#         # Get important properties
#         node_info = {
#             'node_id': getattr(node, 'node_id', None),
#             'text': getattr(node, 'text', None),
#             'metadata': getattr(node, 'metadata', None),
#         }
        
#         # Add any start/end char indexes if available
#         if hasattr(node, 'start_char_idx'):
#             node_info['start_char_idx'] = node.start_char_idx
#         if hasattr(node, 'end_char_idx'):
#             node_info['end_char_idx'] = node.end_char_idx
        
#         # Write formatted output
#         for key, value in node_info.items():
#             f.write(f"\n{key}:\n")
#             if isinstance(value, dict):
#                 f.write(json.dumps(value, indent=2))
#             else:
#                 f.write(str(value))
#             f.write("\n")
        
#         f.write(f"{'='*80}\n")
