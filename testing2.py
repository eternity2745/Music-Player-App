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


os.environ['OPENAI_API_KEY'] = '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'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

template = """
You are a fun chatbot in a music player app and helps user's with their queries.
You're name is Aeris.

Context:
{entities}

Current conversation:
{history}
Last line:
Human: {input}
You:
"""

# llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.3)
# agent = create_csv_agent(llm=llm, path='test.csv', verbose=False)
# memory = ConversationEntityMemory(llm=llm)
llm = HuggingFaceHub(repo_id='mosaicml/mpt-7b-chat',
                     model_kwargs={"temperature": 0, "max_length": 512})
new_memory = ConversationEntityMemory(llm=llm)
print(1)
conversation = LLMChain(
    memory=new_memory, llm=llm, prompt=PromptTemplate(input_variables=['entities', 'history', 'input'], template=template))
# onversation.add_agent(agent)

# print(conversation.prompt.template)


while True:
    s = input("User: ")

    if s != 'exit':
        output = conversation.run(input=s)
        print(2)
        print(output)
        new_memory.save_context(
            {'inputs': s},
            {'outputs': output}

        )
    else:
        print(new_memory)
        print("Ba bai take care and have a nice day")
        break
