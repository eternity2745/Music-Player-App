from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd
import openai
import subprocess
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

os.environ['OPENAI_API_KEY'] = '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'
# openai.api_key = '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'

# dburl = 'mysql+pymysql://root:@localhost/musicplayer'
# db = SQLDatabase.from_uri(dburl)
path = 'test.csv'
llm = OpenAI(temperature=0)
agent = create_csv_agent(llm=llm, path=path, verbose=False)
# agent = SQLDatabaseChain(llm=llm, database=db, verbose=True)
x = agent.run("Sonal have been listening to songs like Nangeli Poove, Thathaka theithare, Arike Ninna, Pottu thotta pournami. Suggest 5 songs which he should listen to next and why?")
print(x)
# agent.run("Explain quantum computing in simple terms ( from your knowledge not using the provided pandas dataframe)")
# agent.run("Abhishek's music history is Nangeli Poove, Sarvam Sadha, Kaathirunnu, Kaliyuga suggest 5 more songs other than the songs in his music history that he would like to listen from songs table along with song id.Your answer should be in sqlresult format.")
# print(x.split('Final Answer: '))
# agent.run("What do you know about the character harry potter? ( answer directly without sql quesry or set sql quesry to select * from users from your knowlegde)")
# messages = [
#    SystemMessage(
#        content='You are a funny chatbot that answers to users queries and remembers everything that user told you'),
#    HumanMessage(content='heya whats your name?')
# ]

# llm(messages)

# while True:
# s = input("User: ")
#   if s != 'exit':
#       llm(messages.append(HumanMessage(content=s)))
#   else:
#       break

# df = pd.read_csv("test.csv")

# prepared_data = df.loc[::]
# prepared_data.rename(
#    columns={'genre': 'prompt', 'title': 'completion'}, inplace=True)
# prepared_data.to_csv('prepared_data.csv', index=False)

# prepared_data.csv --> prepared_data_prepared.json
# openai.api_key = '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'
# subprocess.run(
#    'openai tools fine_tunes.prepare_data --file prepared_data.csv --quiet'.split())

# Start fine-tuning
# subprocess.run(
#    'openai api fine_tunes.create --training_file prepared_data_prepared.jsonl --model davinci --suffix "SuperHero"'.split())
# subprocess.run('openai api fine_tunes.follow -i ft-L7aZNH5KtbiXye2gbmb1p88x')

# chat = ChatOpenAI(streaming=True, callbacks=[
# StreamingStdOutCallbackHandler()], temperature=0)

# while True:
#    s = input("User: ")
#    if s != 'exit':
#        resp = chat([HumanMessage(content=s)])
#    else:
#        break
