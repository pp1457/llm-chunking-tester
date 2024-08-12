from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from mupdf_loader import load_documents
from chunkers.recursive_char import split_documents

CHROMA_PATH = "chroma"

def add_to_chroma(chunks: list[Document]):
  db = Chroma(
    persist_directory=CHROMA_PATH, 
    embedding_function=get_embedding_function()
  )
  existing_items = db.get(include=[])
  existing_ids = set(existing_items["ids"])
  print(f"Number of existing documents in DB: {len(existing_ids)}")

  chunks_with_ids = calculate_chunk_ids(chunks)

  new_chunks = []
  for chunk in chunks_with_ids:
    if chunk.metadata["id"] not in existing_ids:
      new_chunks.append(chunk)
  
  if len(new_chunks):
    print(f"👉 Adding new documents: {len(new_chunks)}")
    new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
    db.add_documents(new_chunks, ids=new_chunks_ids)
    db.persist()
  else:
    print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
  last_page_id = None
  current_chunk_index = 0

  for chunk in chunks:
    source = chunk.metadata.get("source")
    page = chunk.metadata.get("page")
    current_page_id = f"{source}:{page}"

    if (current_page_id == last_page_id):
      current_chunk_index += 1
    else:
      current_chunk_index = 0
    
    last_page_id = current_page_id

    chunk_id = f"{current_page_id}:{current_chunk_index}"

    chunk.metadata["id"] = chunk_id 
  
  return chunks

documents = load_documents()

print("Loaded Documents")

chunks = split_documents(documents)

print("Documents Splitted")

add_to_chroma(chunks)
