from django_rq import job
from utils.lang_chain import LangChainConnector


@job
def parse_pdf_task(pdf_urls):
    parser = LangChainConnector()
    parser.ingest_pdf(pdf_urls)
