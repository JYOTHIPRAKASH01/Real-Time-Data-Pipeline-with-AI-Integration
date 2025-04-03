from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

# Function to create LangChain pipeline for AI processing
def langchain_pipeline(data):
    # Define the prompt template for LangChain
    prompt_template = "Analyze and summarize the following data: {data}"
    prompt = PromptTemplate(input_variables=["data"], template=prompt_template)

    # Initialize the OpenAI language model
    llm = OpenAI(temperature=0.7)

    # Create the LangChain LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain for each data point
    results = []
    for item in data:
        result = chain.run({"data": item})
        results.append(result)
    
    return results

# Example data (replace with real-time processed data)
sample_data = ["Sensor 1: Temp=30C", "Sensor 2: Humidity=60%"]

# Get AI insights from LangChain
insights = langchain_pipeline(sample_data)

# Output the results
for insight in insights:
    print("AI Insight: ", insight)
