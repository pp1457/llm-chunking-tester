import pymupdf4llm
import pathlib
from langchain_community.document_loaders import UnstructuredMarkdownLoader

def load_documents(): 
    md_text = pymupdf4llm.to_markdown("source/frankenstein.pdf")
    pathlib.Path("tmp/output.md").write_bytes(md_text.encode())
    print("📚 Saving markdown to tmp/output.md")
    loader = UnstructuredMarkdownLoader("tmp/output.md")
    print("📚 Loading documents from PDF")
    return loader.load()

