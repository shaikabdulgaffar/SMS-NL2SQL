import os
import re
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

def extract_sql(text):
    """
    Extracts the SQL code from a Markdown code block or plain text.
    Removes leading/trailing backticks and 'sql' language hints if present.
    Also fixes table names generated by Gemini to match your actual Django tables.
    """
    # Try to find SQL code in a code block (```sql ... ```)
    code_block = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if code_block:
        sql = code_block.group(1).strip()
    else:
        # Remove any leading or trailing backticks and 'sql'
        sql = re.sub(r"^```(?:sql)?|```$", "", text, flags=re.IGNORECASE | re.MULTILINE).strip()
    
    # Fix table names: replace 'FROM students' with 'FROM students_student', etc.
    # Add more replacements below if model uses other wrong table names.
    sql = re.sub(r'\bFROM students\b', 'FROM students_student', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bFROM departments\b', 'FROM students_department', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bJOIN students\b', 'JOIN students_student', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bJOIN departments\b', 'JOIN students_department', sql, flags=re.IGNORECASE)
    # And for other possible table aliases:
    sql = re.sub(r'\bFROM student\b', 'FROM students_student', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bFROM department\b', 'FROM students_department', sql, flags=re.IGNORECASE)

    # Fix GROUP_CONCAT to STRING_AGG for PostgreSQL
    sql = re.sub(
        r'GROUP_CONCAT\s*\(\s*([a-zA-Z0-9_\.]+)\s*\)',
        r'STRING_AGG(\1, \',\')',
        sql,
        flags=re.IGNORECASE
    )

    return sql

def nl2sql_query(nl_query, schema_description):
    """
    Uses Gemini 1.5 Flash to convert a natural language query to SQL.

    Args:
        nl_query (str): The user's natural language query.
        schema_description (str): String description of your database schema.

    Returns:
        str: The generated SQL query.
    """
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = (
        f"Convert the following natural language query into an SQL query for the database schema below.\n"
        f"Use these exact table and column names for Django:\n"
        f"{schema_description}\n"
        f"Use PostgreSQL syntax (for example, use STRING_AGG instead of GROUP_CONCAT).\n"
        f"Query: {nl_query}\n"
        f"SQL:"
    )
    response = model.generate_content([prompt])
    sql = extract_sql(response.text)
    return sql