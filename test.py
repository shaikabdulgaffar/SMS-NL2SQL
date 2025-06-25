import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# PostgreSQL URI (Django settings ke hisab se)
db = SQLDatabase.from_uri(
    "postgresql+psycopg2://shaikabdulgaffar:9581@localhost:5432/university_nl2sql"
)

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    handle_parsing_errors=True,
)

result = agent_executor.invoke({"input": "mathematics department me kitne students hain?"})
print(result)