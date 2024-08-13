import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter

def load_documents(): 
    md_text = pymupdf4llm.to_markdown("source/data.pdf")
    print("Converted to Markdown")
    loader = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
        ],
        return_each_line=True
    )
    print("Splitted with Markdown Headers")
    return loader.split_text(md_text)
