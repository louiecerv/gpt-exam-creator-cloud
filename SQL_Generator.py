import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os

client = AsyncOpenAI(
    # This is the default and can be omitted    
    api_key=os.getenv("API_KEY"),
)
  
async def generate_response(question, context):
  model = "gpt-4-0125-preview"
  #model - "gpt-3.5-turbo"

  completion = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": question}, {"role": "system", "content": context}])
  return completion.choices[0].message.content

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

  # Define your default text
  dbschema = """CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
    );

    CREATE TABLE customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20),
        address VARCHAR(255)
    );

  CREATE TABLE orders (
      order_id INT AUTO_INCREMENT PRIMARY KEY,
      customer_id INT NOT NULL,
      order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
  );

  CREATE TABLE order_details (
      order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
      order_id INT NOT NULL,
      product_id INT NOT NULL,
      quantity INT NOT NULL,
      price_per_unit DECIMAL(10, 2) NOT NULL,
      total_price DECIMAL(10, 2) NOT NULL,
      FOREIGN KEY (order_id) REFERENCES orders(order_id),
      FOREIGN KEY (product_id) REFERENCES products(product_id)
  );"""

  # Create the text area with the default value
  user_schema = st.text_area("Enter the database schema:", dbschema)

  options = ['What is the total revenue generated in the last quarter (by order date)?', 
    'What is the average order value (total price) for the last month (by order date)?', 
    'Which product has the highest total quantity sold overall?', 
    'Who is the customer with the most orders placed?',
    'What city/area (derived from address field in customers table) has the most customers?'
    'What is the best-selling product in each month for the last 3 months?',
    'Which products have a stock quantity below a certain threshold (e.g., 10)?',
    'What is the total revenue generated from each customer in the last year (by order date)?',
    'What is the most frequent combination of product purchased together (based on order_details)?',
    'Compare total revenue generated by new vs. returning customers (based on first order date)']
  
  # Create the combobox (selectbox) with a descriptive label
  selected_option = st.selectbox(
      label="Choose an option:",
      options=options,
      index=0  # Optionally set a default selected index
  )

  question = selected_option

  # Create a checkbox and store its value
  checkbox_value = st.checkbox("Input your own query in natural language")

  # Display whether the checkbox is checked or not
  if checkbox_value:
    # Ask the user to input text
    question = st.text_input("Please input a data analytics question/request in natural language:")

  # Text area input for the context
  context = """Follow the instructions exactly. Using the following database schema,give me MYSQL
  SQL statement that will statisfy the question. The SQL must use only the data defined in the schema. 
  Return only the SQL statement without any explanation or other outputs: """ + user_schema

  # Button to generate response
  if st.button("Generate SQL"):
      if question and context:
          response = await generate_response(question, context)
          st.write("Response:")
          st.write(response)
      else:
          st.error("Please enter both question and context.")

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
