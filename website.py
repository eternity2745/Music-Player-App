import streamlit as st
from langchain.chains import SQLDatabaseSequentialChain
from langchain import HuggingFaceHub
import ast
from langchain.tools import StructuredTool
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
import pyjokes
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.prompts.chat import BaseMessagePromptTemplate
from langchain.prompts.base import BasePromptTemplate
from langchain.agents import OpenAIFunctionsAgent, StructuredChatAgent
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents import LLMSingleActionAgent
from langchain import LLMChain
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
import faiss
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from datetime import datetime
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd
import openai
import subprocess
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts.prompt import PromptTemplate
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
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

from langchain.utilities import SerpAPIWrapper

global agent_chain
os.environ['SERPAPI_API_KEY'] = "edad3081de97572290efcd436f7b82de90f0bef23ccf17de73a283d9d77d1bce"

repo_id = "google/flan-t5-xl"
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
os.environ['OPENAI_API_KEY'] = "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"


def processThought(thought):
    return thought


prefix = "You are Aeris, A multifunctional chatbot that tends to user's queries and has the ability to code on your own."
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Use it only when you need info about any ongoing or current event. Ask targeted questions",
    )
]
llm = ChatOpenAI(temperature=0.5,
                 model="gpt-3.5-turbo-0613", max_tokens=1000)
# )'''
agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, return_direct=True,
                               verbose=True, agent_kwargs={'prefix': prefix})

st.set_page_config(
    page_title="Music Player",
    page_icon='images/ai.png',
    layout="wide"
)

st.title("Hello There Welcome to the demo!")


def user_message(prompt):

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    AI(prompt)


def AI(prompt):
    global agent_chain

    try:

        output = agent_chain.run(input=prompt)
        with st.chat_message('assistant'):
            st.markdown(output)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': output})
    except Exception as e:
        with st.chat_message('assistant'):
            st.markdown("Oops! Ive encountered an error please try again")
            st.session_state.messages.append(
                {'role': 'assistant', 'content': 'Oops! Ive encountered an error please try again'})
            print(e)


def assistant_message(prompt):

    with st.chat_message("assistant"):
        if prompt == "music":
            st.markdown("playing audio")
            st.audio("music/kugramame.mp3")
            # st.session_state.messages.append(
            #    {'role': 'assistant', 'content': "playing audio"})
            st.session_state.messages.append(
                {'role': 'assistant', 'text': 'playing audio', 'music': 'music/kugramame.mp3'})

        elif prompt == "code":
            st.code(body="import streamlit as st\nst.write('hai')",
                    language="python", line_numbers=True)
            st.session_state.messages.append(
                {'role': 'assistant',
                    'code': "import streamlit as st\nst.write('hai')", 'lang': 'python'}
            )
        elif prompt == "image":
            st.image(image='images/Bheeshma Parvam.jpeg')
            st.session_state.messages.append(
                {'role': 'assistant', 'image': 'images/Bheeshma Parvam.jpeg'})
        else:
            st.markdown(prompt)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': prompt})


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "content" in message:
            st.markdown(message["content"])
        elif "music" in message:
            st.markdown(message['text'])
            st.audio(message["music"])
        elif "code" in message:
            st.code(message['code'], message['lang'], line_numbers=True)
        elif "image" in message:
            st.image(message['image'])

prompt = st.chat_input("What do you want?")

if prompt:
    user_message(prompt)
