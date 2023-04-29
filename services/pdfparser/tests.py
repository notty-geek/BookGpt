from django.test import TestCase

# Create your tests here.
import os
from unittest import TestCase, mock
from utils.lang_chain import LangChainConnector


class TestLangChainConnector(TestCase):

    def setUp(self):
        self.pdf_urls = ['http://example.com/document.pdf']
        self.mock_loader = mock.Mock()
        self.mock_loader.load.return_value = ['Document text']
        self.mock_embeddings = mock.Mock()
        self.mock_docs = ['Document text']
        self.mock_text_splitter = mock.Mock()
        self.mock_text_splitter.split_documents.return_value = self.mock_docs
        self.mock_docsearch = mock.Mock()
        self.mock_docsearch.similarity_search.return_value = self.mock_docs
        self.mock_llm = mock.Mock()
        self.mock_chain = mock.Mock()
        self.mock_chain.run.return_value = 'Answer'

    @mock.patch('utils.lang_chain.Pinecone')
    @mock.patch('utils.lang_chain.OnlinePDFLoader')
    @mock.patch('utils.lang_chain.OpenAIEmbeddings')
    @mock.patch('utils.lang_chain.CharacterTextSplitter')
    def test_ingest_pdf(self, mock_text_splitter, mock_embeddings, mock_loader, mock_pinecone):
        # Set up the test
        connector = LangChainConnector()
        mock_text_splitter.return_value = self.mock_text_splitter
        mock_embeddings.return_value = self.mock_embeddings
        mock_loader.return_value = self.mock_loader
        mock_pinecone.from_documents.return_value = None

        # Call the method being tested
        connector.ingest_pdf(self.pdf_urls)

        # Assert that the expected methods are called with the correct arguments
        mock_loader.assert_called_once_with(self.pdf_urls[0])
        mock_loader.return_value.load.assert_called_once_with()
        mock_text_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=0)
        mock_text_splitter.return_value.split_documents.assert_called_once_with(self.mock_docs)
        mock_embeddings.assert_called_once_with(openai_api_key=os.getenv("OPENAI_API_KEY", ))
        mock_pinecone.from_documents.assert_called_once_with(self.mock_docs, self.mock_embeddings,
                                                             index_name=os.getenv("PINECONE_INDEX"))
