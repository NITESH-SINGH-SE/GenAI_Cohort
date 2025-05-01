from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Step_Back:
    def __init__(self) -> None:
        self.step_back_prompt = """
            You are an expert software engineer. 
            Your task is to rephrase the given question into a more general form that is easier to answer.

            # Example 1
            Question: How to improve Django performance?
            Output: what factors impact web app performance?

            # Example 2
            Question: How to optimize browser cache in Django?
            Output: What are the different caching options?

            Question: {question}
            Output:
        """

    def get_relevant_chunks(self, llm, retriever, user_prompt):
        step_back_prompt_template = ChatPromptTemplate.from_template(self.step_back_prompt)

        retrieval_chain = (
            step_back_prompt_template
            | llm
            | StrOutputParser()
            # What is the purpose of the fs module?
            | retriever
        )

        relevant_chunks = retrieval_chain.invoke(
            {"question": user_prompt}
        )

        return relevant_chunks
