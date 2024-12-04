import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection setup
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Home Risk",
            user="postgres",
            password=12345,
            port=5432  # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to execute queries
def execute_query(query):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                if cur.description:  # Check if query returns data
                    columns = [desc[0] for desc in cur.description]
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=columns)
                    return df
                else:
                    conn.commit()
                    return "Query executed successfully."
        except Exception as e:
            return f"Error executing query: {e}"
        finally:
            conn.close()
    else:
        return "Unable to connect to the database."

# Streamlit UI
st.title("PgSQL Database Website Viewer")
st.write("Use this website application to run queries on Home Risk database and view results.")

# Input area for SQL queries
query = st.text_area("Enter your SQL query:", height=200)

if st.button("Execute Query"):
    if query.strip():
        result = execute_query(query.strip())
        if isinstance(result, pd.DataFrame):
            st.success("Query executed successfully!")
            st.dataframe(result)
        else:
            st.error(result)
    else:
        st.warning("Please enter a valid SQL query.")

# Footer
st.write("Developed using Streamlit and PostgreSQL.")
st.write("By Rithwik Gilla, Dheeraj Reddy Redygari, Areef Shaik")
