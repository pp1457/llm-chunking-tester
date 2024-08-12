from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_name: str):
    loader = PyMuPDFLoader(file_name)
    return loader.load()

if __name__ == '__main__':
    pdf_document = load_pdf('source/data.pdf')
    print(pdf_document) 