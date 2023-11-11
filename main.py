import sqlite3
# import random
# Connect to the SQLite database
# conn = sqlite3.connect('tshirts.db')
# cursor = conn.cursor()
#
# # Function to populate t_shirts table
# def populate_t_shirts():
#     counter = 0
#     max_records = 20
#
#     # Seed the random number generator
#     random.seed()
#
#     for i in range(max_records):
#         brand = random.choice(['Van Huesen', 'Levi', 'Nike', 'Adidas'])
#         color = random.choice(['Red', 'Blue', 'Black', 'White'])
#         size = random.choice(['XS', 'S', 'M', 'L', 'XL'])
#         price = random.randint(10, 50)
#         stock = random.randint(10, 100)
#
#         # Attempt to insert a new record
#         # Duplicate brand, color, size combinations will be ignored due to the unique constraint
#         try:
#             cursor.execute("INSERT INTO t_shirts (brand, color, size, price, stock_quantity) VALUES (?, ?, ?, ?, ?)",
#                            (brand, color, size, price, stock))
#             conn.commit()
#
#         except sqlite3.IntegrityError:
#             # Ignore duplicate key error
#             pass
#
# # Call the function to populate the t_shirts table
# # populate_t_shirts()
#
#
# # Execute a SELECT query
# discount_data = [
#     (1, 10.00),
#     (2, 15.00),
#     (3, 20.00),
#     (4, 5.00),
#     (5, 25.00),
#     (6, 10.00),
#     (7, 30.00),
#     (8, 35.00),
#     (9, 40.00),
#     (10, 45.00)
# ]
#
# cursor.executemany("INSERT INTO discounts (t_shirt_id, pct_discount) VALUES (?, ?)", discount_data)
# conn.commit()
#
# cursor.execute("SELECT * FROM discounts")
# rows = cursor.fetchall()
#
# # Print the results
# for row in rows:
#     print(row)
# # Close the connection
# conn.close()
from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import os
from dotenv import load_dotenv
from fewshots import fewshots
load_dotenv()
def sqllm():

    db = SQLDatabase.from_uri(
        "sqlite:///tshirts.db",
        sample_rows_in_table_info=3,
    )
    llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)
    # q1 = db_chain("SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorize = [" ".join(example.values()) for example in fewshots]
    vectorstore = Chroma.from_texts(vectorize,embedding=embeddings,metadatas=fewshots)
    selector=SemanticSimilarityExampleSelector(vectorstore=vectorstore,k=2)
    _mysql_prompt="""You are a database expert. Given an input question, first create a syntactically correct SQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) for MySQL and double quotes (") for SQLite to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful not to query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURRENT_DATE function for MySQL and CURRENT_DATE function for SQLite to get the current date if the question involves "today".
    
    Use the following format:
    
    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here"""

    prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
            template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        )
    few_shot_prompt = FewShotPromptTemplate(
            example_selector=selector,
            example_prompt=prompt,
            prefix=_mysql_prompt,
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"],
        )
    db_chain = SQLDatabaseChain.from_llm(llm,db,verbose=True,prompt=few_shot_prompt)
    return db_chain
if __name__ =="__main__":
    chain = sqllm()

