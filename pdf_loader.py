from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader

def load_documents():
  document_loader = PyPDFDirectoryLoader('./source')
  return document_loader.load()

if __name__ == '__main__':
  documents = load_documents()
  for document in documents:
    print(document)