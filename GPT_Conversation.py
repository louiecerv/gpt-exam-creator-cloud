import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os
import time

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

  context = """You are a teaching co-pilot designed to assist educators in various classroom tasks. 
  When responding to prompts, prioritize providing resources and strategies that directly benefit teachers.
  Remember, your primary function is to empower teachers and enhance their effectiveness in the classroom."""

  options = ['K1', 'K2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 
    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
  
  yearlevel = st.selectbox(
    label="Select year level:",
    options=options,
    index=7  # Optionally set a default selected index
  )

  topic = st.text_input("Please input the topic: ")

  options = ['Generate engaging learning activities', 
    'Suggest alternative explanations for a concept students find challenging', 
    'Provide differentiation strategies to cater to learners with varying needs',
    'Create formative assessment ideas to gauge student understanding',
    'Offer resources for incorporating technology into the classroom']
    
  # Create the combobox (selectbox) with a descriptive label
  selected_option = st.selectbox(
    label="Choose a task for the teaching co-pilot:",
    options=options,
    index=0  # Optionally set a default selected index
  )

  question = selected_option + " for year level " + yearlevel + " on topic " + topic

  # Create a checkbox and store its value
  checkbox_value = st.checkbox("Check this box if you want to input your own prompt.")

  # Display whether the checkbox is checked or not
  if checkbox_value:
    # Ask the user to input text
    question = st.text_input("Please input a prompt (indicate year level and topic): ")

  # Button to generate response
  if st.button("Generate Response"):
    progress_bar = st.progress(0, text="The AI is processing the request, please wait...")
    if question:
      response = await generate_response(question, context)
      st.write("Response:")
      st.write(response)
    else:
      st.error("Please enter a prompt.")

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    st.success("AI processing completed!") 

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
