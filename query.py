import argparse
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
回答以下的問題
---
{question}
--- 
只參考以下內容資料來幫助回答上面的問題，不要使用你的知識，對於每個回答請列出參考資料
--- 
{context}
---
"""

def main():

    query_text = input("Query: ")
    query_rag(query_text)

def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(
      persist_directory=CHROMA_PATH,
      embedding_function=embedding_function
    )
  
    results = db.similarity_search_with_score(query_text, k=5)

    print("\n---\n")
    print("Retrieval Results: ")
    print(results)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
  
    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)
 
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"---\n\nResponse:\n {response_text}\nSources:\n {sources}"
    print(formatted_response)
    return response_text

if __name__ == "__main__":
  main()


