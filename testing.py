# from langchain.chat_models import JinaChat
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd
import openai
import subprocess
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.chains import LLMChain, SQLDatabaseSequentialChain
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
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatGooglePalm
import ast
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCEDrw4PLZvE0iEhoYo6FpNq_QqgofLWfs'
os.environ['OPENAI_API_KEY'] = "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"
# openai.api_key = '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'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

dburl = 'mysql+pymysql://root:@localhost/musicplayer'
db = SQLDatabase.from_uri(dburl, sample_rows_in_table_info=10)
# path = 'test.csv'
llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo-0613')
# print(db.table_info)
# llm = ChatGooglePalm()
# llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct",
#                     model_kwargs={"temperature": 0.5, "max_length": 4096})
# llm = JinaChat(temperature=0)
# agent = create_csv_agent(llm=llm, path=path, verbose=True, replace=True)
agent = SQLDatabaseSequentialChain.from_llm(llm=llm, database=db,
                                            verbose=True, return_direct=True)
# x = agent.run("Recommend 10 other songs other than Nangeli Poove, Mukkathe Penne, Aaromale, Chundari Penne, Thee Minnal which are similar to these songs it should have authors similar to the songs provided also it should be similar to its genre, language use OR or LIKE statements and it order by rand()if you want but there should be exactly 10 songs no matter if the songs doesnt fully match")
# x = agent.run("Abhishek is a user and his listening history of songs is Nangeli Poove, Ambadi Thumbi, Chithirathira, Kaathirunnu, Kugramame, Sree Vinayagam, Sneham Nee Nadha, Kannond Chollanu, Kaathirunnu and Pazham Thamizh find 10 songs other than those that are given in user's listening history in which have similar authors and genres and languages of the songs in user's listening history you can use like or OR to clauses b/w genres or b/w diff authors ( check for atleast 5 different authors ) or b/w diff languages set the limit to 10 and order by rand() and get their song id and song name")
with get_openai_callback() as f:
    x = agent.run(
        "I want to listen to one song that gives me an element of motivation")
    print(x)
    print(f"Tokens Usage\n{f}")
# y = ast.literal_eval(x)
# print(y)
# for i in y:
#    print(f"Song id: {i[0]} |  Song Name: {i[1]}")
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
