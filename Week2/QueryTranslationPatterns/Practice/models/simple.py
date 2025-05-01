class Simple_Query_Translation:
    def __init__(self) -> None:
        self.relevant_docs=None

    def get_relevant_docs(self, vector_store, user_prompt):
        self.relevant_docs = vector_store.similarity_search(user_prompt)
        return self.relevant_docs