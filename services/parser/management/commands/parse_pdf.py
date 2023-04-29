from django.core.management import BaseCommand
from utils.lang_chain import LangChainConnector


class Command(BaseCommand):
    """Sync plans from stripe."""

    help = "Sync Subscription from stripe."

    def handle(self, *args, **options):
        pdf_urls = [
            "https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf",
            "https://www.thisisclassicalguitar.com/wp-content/uploads/2021/03/Classical-Guitar-Method-Vol1-2020.pdf"
        ]
        parser = LangChainConnector()
        parser.ingest_pdf(pdf_urls)
        # parser.query("What is C Chord?")
