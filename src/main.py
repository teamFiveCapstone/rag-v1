from services.document_ingester import DocumentIngester


def main (file_path): 
    ingester = DocumentIngester()
    ingester.process_document(file_path)

# main("../files/wild_animals/lion.pdf")
main("../files/domestic_animals/cat.pdf")