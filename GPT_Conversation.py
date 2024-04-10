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

  # Convert chat history to a list of dictionaries
  chat_history_list = [{"role": message["role"], "content": message["content"]} for message in chat_history.history]

  # Add user question and previous context to history (list format)
  chat_history_list.append({"role": "user", "content": question})

  # Include full chat history in the prompt
  prompt = context + "\n" + question

  # monitor what's going on (optional)
  print(prompt)

  completion = await client.chat.completions.create(model=model, messages=chat_history_list)
  # Update context with system response
  context = completion.choices[0].message.content
  chat_history.add_message("system", context)
  return context

async def app():
  st.subheader("Teacher Co-pilot")

  text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
  CCS 229 - Intelligent Systems
  Department of Computer Science
  College of Information and Communications Technology
  West Visayas State University"""
  st.text(text)

  st.image("teach-copilot.png", caption="A Teacher Co-pilot")
  
  text = """Empower your learning journey with an AI-powered copilot!
  \nThis innovative data app leverages the power of Streamlit and OpenAI's ChatGPT 
  to create a one-of-a-kind educational experience. Imagine a chat interface where you can:
  * Ask questions: Get clear and informative answers to your learning inquiries across various subjects.
  * Practice concepts: Engage in interactive exercises and receive real-time feedback from your AI companion.
  * Spark creativity: Brainstorm ideas, explore diverse perspectives, and unlock new approaches to problem-solving.
  * Boost confidence: Receive personalized guidance and overcome learning roadblocks with the support of your AI coach.
  \nStudents seeking an on-demand learning assistant Educators looking to enhance their teaching methods
  Anyone curious to explore the potential of AI for learning"""
  st.write(text)

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
