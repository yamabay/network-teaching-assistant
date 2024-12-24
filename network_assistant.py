from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from typing import Literal
from operator import itemgetter
from pydantic import BaseModel, Field


# Ask your question here
question = "What is the Internet?"


# Define the LLM to use in the chain
llm = ChatOllama(
    model = "llama3.1",
    base_url = "http://localhost:11434",
)


# Define the prompt templates for the different routes in the chain
expert_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert instructor in computer networking. You can assume the user is also at the expert level. Clearly note 'Expert' at the beginning of your response."),
        ("human", "{question}"),
    ]
)

beginner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an instructor in computer networking for beginners. You should assume the user is at the beginner level. Clearly note 'Beginner' at the beginning of your response."),
        ("human", "{question}"),
    ]
)


# Define the chains for each route
expert_chain = expert_prompt | llm | StrOutputParser()
beginner_chain = beginner_prompt | llm | StrOutputParser()



# System template for initial route determination
primary_route_system_template = """
You should only return the word 'expert' or 'beginner' in all lowercase based on the level of difficulty/expertise of the question.
Examples:
Question: What is a router? Answer: beginner
Question: What are the fields in an IPSec header? Answer: expert
Question: What is a routing protocol? Answer: beginner
"""


# Define the initial prompt for the first chain step
primary_route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", primary_route_system_template),
        ("human", "{question}"),
    ]
)


# Define the initial chain
# Model will return the destination and justification attributes
# The justification attribute is just for testing if the model is not behaving as intended
route_chain = (
    primary_route_prompt
    | llm
    | RunnableLambda(lambda output: output.content)
)


# Full chain definition, determine the appropriate level (route_chain), and run that level's chain
chain = {
    "destination": route_chain,
    "question": lambda x: x["question"],
} | RunnableLambda(
    lambda x: expert_chain if x["destination"] == "expert" else beginner_chain
)


# Use this to text the route_chain (see what level the model thinks the question is at)
#result = route_chain.invoke({"question": "How much latency is introduced on average by the processing time for IPSec packets? I am an expert"})


# Run the full chain
result = chain.invoke({"question": question})
print(result)
