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
  st.subheader("AI-enabled Exam Creator")

  text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
  CCS 229 - Intelligent Systems
  Department of Computer Science
  College of Information and Communications Technology
  West Visayas State University"""
  st.text(text)



  text = """Introducing the GPT Exam Creator, a user-friendly tool powered by 
  Chat-GPT and Streamlit that empowers educators to effortlessly generate 
  custom exams tailored to their students' needs. With this innovative platform, 
  instructors can select the year level, topic, and type of exam they desire 
  to create. Whether it's a comprehensive test covering multiple subjects for 
  high school seniors or an essay quiz for middle 
  schoolers, the GPT Exam Creator streamlines the process.
  By leveraging the vast knowledge of Chat-GPT, the generated questions are 
  not only accurate but also engaging, ensuring that students are challenged 
  while learning. Plus, the intuitive interface of Streamlit makes navigation 
  seamless, allowing educators to concentrate on crafting the perfect 
  assessment without any technical hassle.
  Revolutionize your exam preparation process with the GPT Exam Creator and 
  empower your students to excel academically like never before."""
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

  options = ['Multiple Choice', 
    'True or False', 
    'Short Phrase',
    'Essay',
    'Matching Type']
    
  # Create the combobox (selectbox) with a descriptive label
  selected_option = st.sidebar.selectbox(
    label="Select the exam type:",
    options=options,
    index=0  # Optionally set a default selected index
  )

  st.sidebar.write("**(c) 2024 - The AI Research Lab** West Visayas State University")

  if selected_option=="Multiple Choice":
    type = "create 10 multiple-choice quiz with 4 options. Provide the answer key."
  elif selected_option=="True or False":
    type = "create 10 true or false type quiz. Provide the answer key."
  elif selected_option=="Short Phrase":
    type = "create 10-item short-phrase type quiz. Provide the answer key."
  elif selected_option=="Essay":
    type = "create an essay quiz. Provide the scoring rubric."
  elif selected_option=="Matching Type":
    type = "create a 10-item matching type quiz. Provide the answer key."

  question = "For year level " + yearlevel + " on topic " + topic + " " + type

  # Create a checkbox and store its value
  checkbox_value = st.checkbox("Check this box if you want to input your own prompt.")

  # Display whether the checkbox is checked or not
  if checkbox_value:
    # Ask the user to input text
    question = st.text_input("Please input a prompt (indicate year level and topic): ")

  # Button to generate response
  if st.button("Create"):
    progress_bar = st.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
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
    st.success("AI teacher co-pilot has created your quiz!") 

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
