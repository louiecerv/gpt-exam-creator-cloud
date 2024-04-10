import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os

client = AsyncOpenAI(  
    api_key=os.getenv("API_KEY"),
)

class ChatHistory:
  def __init__(self):
    self.history = []

  def add_message(self, role, content):
    self.history.append({"role": role, "content": content})

  def get_history_text(self):
    history_text = ""
    for message in self.history:
      history_text += f"{message['role']}: {message['content']}\n"
    return history_text.strip()
  
chat_history = ChatHistory()

async def generate_response(question, context):
  model = "gpt-4-0125-preview"

  # Add user question and previous context to history
  chat_history.add_message("user", question)

  # Include full chat history in the prompt
  prompt = chat_history.get_history_text() + "\n" + context

  completion = await client.chat.completions.create(model=model, messages=[[prompt]])
  # Update context with system response
  context = completion.choices[0].message.content
  chat_history.add_message("system", context)
  return context


async def app():
  st.subheader("AI-Driven SQL Query Generator")

  text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
  CCS 229 - Intelligent Systems
  Department of Computer Science
  College of Information and Communications Technology
  West Visayas State University"""
  st.text(text)

  st.image("ai-sql.jpg", caption="AI-Driven Analytics")
  
  text = """
  \nThe AI-Driven SQL Query Generator is a Streamlit web application that showcases the capabilities of 
  an AI model to generate SQL queries based on a provided database schema. This app serves as a 
  precursor to AI-driven data analytics, enabling users to input their data requests in natural 
  language and receive corresponding SQL queries that can be executed by the database engine to 
  fulfill the request.
  \nFeatures:
  \n1. Database Schema Input - Users can upload or input the schema of their database. This schema includes 
  information about tables, columns, data types, and relationships between tables.
  \n2. Natural Language Input - Users can input their data request in natural language using text 
  input fields. For example, they could input queries like "Show me the total sales for each product 
  in the past month" or "Retrieve the top 10 customers by total purchase amount".
  \n3. AI Model Integration - The application integrates a trained AI model that converts natural 
  language queries into SQL queries. The model is capable of understanding various query structures 
  and generating corresponding SQL code that can retrieve the requested data from the database.
  \n4. SQL Query Output - Once the user submits their natural language query, the AI model processes 
  it and generates the corresponding SQL query. The generated SQL query is displayed to the user, 
  allowing them to review and potentially modify it if needed.
  \n5. Query Execution- Optionally, users can choose to execute the generated SQL query directly against their database. 
   This feature provides real-time feedback on the data returned by the query, helping users validate 
   the accuracy of the generated SQL code.
   \n6. User Feedback - The app provides a feedback mechanism for users to report any inaccuracies or 
   improvements in the generated SQL queries. This feedback loop helps improve the performance and 
   accuracy of the AI model over time.
   \nVisualization - To enhance user experience, the app may include visualization capabilities to 
   display query results in interactive charts, graphs, or tables. This allows users to gain insights 
   from the retrieved data more easily.
   \nThe AI-Driven SQL Query Generator empowers users to interact with their database using natural 
   language, bridging the gap between non-technical users and complex database systems. It lays the 
   foundation for future advancements in AI-driven data analytics, making data access and analysis 
   more intuitive and efficient."""
  with st.expander("Click her for more information."):
    st.write(text)


  st.title("OpenAI Text Generation App")

  # Text input for user question
  question = st.text_input("Enter your question:")

  # Button to generate response
  if st.button("Generate Response"):
    if question:
      response = await generate_response(question, "")
      st.write("Response:")
      st.write(response)
    else:
      st.error("Please enter a question.")

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
