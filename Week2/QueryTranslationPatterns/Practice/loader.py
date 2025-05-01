class Loader:
    def __init__(self, file_path, document_loader) -> None:
        self.file_path = file_path
        self.loader = document_loader(file_path)
    
    def load_file(self):
        return self.loader.load()