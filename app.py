import streamlit as st
import openai
import sqlite3
import pandas as pd
from io import StringIO

# Global database name
db_name = "st.db"

# Initialize session state variables
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "data_processed" not in st.session_state:
    st.session_state.data_processed = False

# Sidebar for OpenAI API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# Check if key is entered or is valid
if openai_api_key and not st.session_state.api_key_valid:
    try:
        openai.api_key = openai_api_key
        openai.models.list()
        st.session_state.api_key_valid = True
    except openai.error.APIError:
        st.error("Invalid API key. Please enter a valid OpenAI API key.")

if st.session_state.api_key_valid:
    st.sidebar.success("API key is valid.")

    # Main content
    st.title("AI-Powered SQL Query Generator")

    # Input table data in CSV format
    data = st.text_area("Enter table data in CSV format:", value="""EmployeeID,FirstName,LastName,Age,Department,Position,Salary,HireDate,ManagerID
1,John,Smith,25,IT,Developer,50000,2022-01-01,2
2,Emily,Johnson,30,Marketing,Manager,80000,2022-02-01,3
3,Michael,Williams,35,Sales,Analyst,60000,2022-03-01,1
""")

    # Button to process table data
    if st.button("Process Table Data"):
        data = pd.read_csv(StringIO(data))
        table_data = data.values.tolist()
        st.write("Extracted Table Data:")
        st.table(data)

        # Create and populate database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS employees')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            EmployeeID INTEGER PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            Age INTEGER,
            Department TEXT,
            Position TEXT,
            Salary INTEGER,
            HireDate TEXT,
            ManagerID INTEGER
        )
        ''')
        cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', table_data)
        conn.commit()
        conn.close()

        st.success("Database created and populated successfully!")
        st.session_state.data_processed = True

    if st.session_state.data_processed:
        # Schema
        schema = """
        CREATE TABLE employees (
            EmployeeID INTEGER PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            Age INTEGER,
            Department TEXT,
            Position TEXT,
            Salary INTEGER,
            HireDate TEXT,
            ManagerID INTEGER
        );
        """

        # Input natural language question
        question = st.text_area("Enter natural language question:", value="What is the average salary of the IT department?")

        # Function to generate SQL using OpenAI
        def generate_sql(question, schema):
            prompt=f"""
                f"Given the following SQL schema: 
                {schema}
                Write a SQL query to {question}"
                """
            response = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",  
                    prompt=prompt,
                    temperature=0,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
            sql_query = response.choices[0].text.strip()
            return sql_query

        # Function to optimize SQL using OpenAI
        def optimize_sql(sql_query):
            prompt=f"""
                Optimize this SQL query using using indexes, optimizing joins or other techniques.
                Only give the resulting sql, for the question: {sql_query} 
                """
            response = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
            optimized_query = response.choices[0].text.strip()
            return optimized_query


        # Function to execute SQL query
        def execute_sql(db_name, query):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            results = []
            for statement in query.split(';'):
                if statement.strip():
                    cursor.execute(statement.strip())
                    if statement.strip().lower().startswith("select"):
                        results.extend(cursor.fetchall())
            conn.close()
            return results

        # Button to generate SQL
        if st.button("Generate SQL"):
            if question:
                sql_query = generate_sql(question, schema)
                st.write("Generated SQL Query:")
                st.code(sql_query)

                # Optimize SQL
                optimized_sql = optimize_sql(sql_query)
                st.write("Optimized SQL Query:")
                st.code(optimized_sql)

                # Execute SQL
                results = execute_sql(db_name, sql_query)
                st.write("Query Results:")
                st.write(results)

                # Execute the optimized SQL
                optimized_results = execute_sql(db_name, optimized_sql)
                st.write("Optimized Query Results:")
                st.write(optimized_results)
            else:
                st.warning("Please enter a question.")
