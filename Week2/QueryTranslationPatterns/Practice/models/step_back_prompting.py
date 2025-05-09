from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Step_Back:
    def __init__(self) -> None:
        self.step_back_prompt = """
            You are an expert at world  knowledge. 
            Your task is to rephrase the given question into a more general form that is easier to answer.

            # Example 1
            Question: How to improve Django performance?
            Output: what factors impact web app performance?

            # Example 2
            Question: How to optimize browser cache in Django?
            Output: What are the different caching options?

            # Example 3
            Question: Which position did Knox Cunningham hold from May 1955 to Apr 1956?
            Output: Which positions have Knox Cunning- ham held in his career?

            # Example 4
            Question: Who was the spouse of Anna Karina from 1968 to 1974?
            Output: Who were the spouses of Anna Karina?

            # Example 5
            Question: Which team did Thierry Audel play for from 2007 to 2008?
            Output: Which teams did Thierry Audel play for in his career?

            Question: {question}
            Output:
        """

    def get_relevant_chunks(self, llm, retriever, user_prompt):
        step_back_prompt_template = ChatPromptTemplate.from_template(self.step_back_prompt)

        retrieval_chain = (
            step_back_prompt_template
            | llm
            | StrOutputParser()
            # How does changing temperature and volume affect the pressure of an ideal gas?
            | retriever
        )

        relevant_chunks = retrieval_chain.invoke(
            {"question": user_prompt}
        )

        return relevant_chunks
