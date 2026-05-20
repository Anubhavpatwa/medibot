from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings

import fitz



# LOAD EMBEDDING MODEL

embedding_model = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)



# FUNCTION TO STORE PDF DATA

def process_pdf(pdf_path):

    text = ""

    pdf = fitz.open(pdf_path)

    for page in pdf:

        text += page.get_text()



    # SPLIT TEXT INTO CHUNKS

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=300,

        chunk_overlap=30

    )



    chunks = splitter.split_text(text)



    # STORE IN CHROMADB

    vectordb = Chroma.from_texts(

        texts=chunks,

        embedding=embedding_model,

        persist_directory="chromadb"

    )



    vectordb.persist()



    return "PDF processed successfully."



# SEARCH FUNCTION

def search_pdf(query):

    vectordb = Chroma(

        persist_directory="chromadb",

        embedding_function=embedding_model

    )



    docs = vectordb.similarity_search_with_score(
    query,
    k=5
    )



    context = "\n".join(
    [doc[0].page_content for doc in docs]
)



    return context