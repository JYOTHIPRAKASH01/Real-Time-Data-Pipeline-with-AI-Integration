from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import snowflake.connector

# Snowflake Connection
conn = snowflake.connector.connect(
    user='<your_snowflake_user>',
    password='<your_snowflake_password>',
    account='<your_snowflake_account>',
    warehouse='COMPUTE_WH',
    database='REAL_TIME_DB',
    schema='PUBLIC'
)

# Fetch real-time processed data from Snowflake
query = "SELECT * FROM REAL_TIME_TABLE"
cursor = conn.cursor()
cursor.execute(query)
data = cursor.fetchall()

# Prepare LangChain Prompt Template for analysis
prompt_template = "Analyze the following sensor data and provide insights: {data}"
prompt = PromptTemplate(template=prompt_template, input_variables=["data"])

# Initialize OpenAI and LangChain LLM
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# Process the data with LangChain
analysis_results = []
for row in data:
    sensor_data = row[1:]  # Adjust based on Snowflake schema
    result = chain.run({"data": str(sensor_data)})
    analysis_results.append(result)

# Print AI insights
for result in analysis_results:
    print(f"AI Insights: {result}")
