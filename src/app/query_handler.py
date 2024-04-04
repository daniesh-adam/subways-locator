"""
Contains the QueryHandler class to handle queries to SQL database using llm.

"""


from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_fireworks import ChatFireworks


class QueryHandler:
    """
    A class to handle queries to a SQL database using a language model.
    """

    def __init__(self, dburi: str, fireworks_api_key) -> None:
        """
        Initializes the QueryHandler with database URI and Fireworks API key.

        Args:
            dburi (str): The URI of the SQL database.
            fireworks_api_key: The API key for the Fireworks language model.
        """
        self.db = SQLDatabase.from_uri(dburi)
        self.llm = ChatFireworks(
            model="accounts/fireworks/models/firefunction-v1",
            fireworks_api_key=fireworks_api_key, temperature=0)
        self.chain = self.create_chain()

    def create_chain(self) -> RunnableSerializable[any, str]:
        """
        Creates a chain of operations to handle a query.

        Returns:
            RunnableSerializable[any, str]: A chain of operations.
        """
        write_query = create_sql_query_chain(self.llm, self.db)
        execute_query = QuerySQLDataBaseTool(db=self.db)
        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, \
                and SQL result, answer the user question.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
        )
        answer = answer_prompt | self.llm | StrOutputParser()
        chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer
        )
        return chain

    def get_response(self, question: str) -> str:
        """
        Gets a response to a question by invoking the chain of operations.

        Args:
            question (str): The question to respond to.

        Returns:
            str: The response to the question.
        """
        response = self.chain.invoke({"question": question})
        return response


if __name__ == "__main__":

    DBURI = "sqlite:///app/data/outlets.db"
    query_handler = QueryHandler(
        dburi=DBURI,
        # ! API key
        fireworks_api_key="SqBWv34DVdUJFGpIWO6IXvgDzCpeHvjMXcsRm6IIJScUGOHx")

    QUESTION = "Where is Subway Menara UOA Bangsar?"
    result = query_handler.get_response(question=QUESTION)

    print(result)
    # Subway Menara UOA Bangsar is located at Jalan Bangsar Utama 1,
    # Unit 1-2-G, Menara UOA Bangsar, Kuala Lumpur, 59000.
