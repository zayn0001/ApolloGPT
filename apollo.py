from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import requests

question = "Who is the current home minister of kerala"

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key="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")
messages = [
    SystemMessage(content="For every question i ask, provide nothing but a single sentence which is by converting it a search query"),
    HumanMessage(content=question)
]


response = chat(messages)

from bs4 import BeautifulSoup 
  
  


query = response.content
print(query)

url = "https://www.googleapis.com/search"

# Define parameters as a dictionary
parameters = {
    'q': query
}


r = requests.get(url, params=parameters)

soup = BeautifulSoup(r.content, 'html.parser') 

soup.find('h2', string='Featured snippet from the web')


content = ""

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key="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")

messages = [
    SystemMessage(content=""),
    HumanMessage(content=content)
]


response = chat(messages)

print(response.content)