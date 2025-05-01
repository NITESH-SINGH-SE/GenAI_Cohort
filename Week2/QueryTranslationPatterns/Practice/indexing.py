class Indexer:
    def __init__(self, document, text_splitter) -> None:
        self.document = document
        # self.retriever = ""
        # self.temperature = ""
        self.text_splitter = text_splitter
        self.docs = None

    def chunking(self):
        self.docs = self.text_splitter.split_documents(self.document)
        return self.docs
        