import os
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone


class LangChainConnector:

    def __init__(self, chunk_size=1000, chunk_overlap=0):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", )
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_index = os.getenv("PINECONE_INDEX")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        pinecone.init(
            api_key=self.pinecone_api_key,  # find at app.pinecone.io
            environment=os.getenv("PINECONE_API_ENV")  # next to api key in console
        )

    def ingest_pdf(self, pdfs):
        for pdf in pdfs:
            loader = OnlinePDFLoader(pdf)
            documents = loader.load()
            embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            Pinecone.from_documents(docs, embeddings, index_name=self.pinecone_index)

    def query(self, query):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        docsearch = Pinecone.from_existing_index(self.pinecone_index, embeddings)
        docs = docsearch.similarity_search(query)
        llm = OpenAI(temperature=0.9, openai_api_key=self.openai_api_key)
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=docs, question=query)
        return answer
