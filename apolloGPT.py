from fastapi import FastAPI
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import requests
from bs4 import BeautifulSoup 
import re
from mangum import Mangum






def get_query(question):

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key="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")
    messages = [
        SystemMessage(content="For every question i ask, provide nothing but a single sentence which is by converting the input into a google search query"),
        HumanMessage(content=question)
    ]
    response = chat(messages)
    query = response.content
    return query

def get_searchresults(query):



    url = "https://www.google.com/search"

    parameters = {
        'q': query
    }


    r = requests.get(url, params=parameters)
    soup = BeautifulSoup(r.content, 'html.parser') 

    def get_featured():
        k = soup.find_all("div", class_="BNeawe")
        text = str(k[0])
        pattern = r'>(.*?)<'
        matches = re.findall(pattern, text)
        info = "".join(matches)
        return info

    def get_titles():
        k = soup.find_all("div", class_="vvjwJb")
        k = [str(x) for x in k]
        text = ". ".join(k)
        pattern = r'>(.*?)<'
        matches = re.findall(pattern, text)
        info = "".join(matches)
        return info


    titles = get_titles()
    featured = get_featured()
    return titles+featured

def get_response(question, shi):

    content = "The answer to the question is hidden somewhere in the data given below. The data is as follows: '" + shi + "'.  The question is as follows: '" + question + "'"

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key="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")

    messages = [
        SystemMessage(content=""),
        HumanMessage(content=content)
    ]


    response = chat(messages)

    return response.content


app = FastAPI()
handler = Mangum(app)

@app.get("/{message}")
async def root(message: str):
    query  = get_query(message)
    sr = get_searchresults(query)
    res = get_response(message, sr)
    return {"message": message, "response":res}