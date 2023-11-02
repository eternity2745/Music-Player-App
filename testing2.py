from langchain.chat_models import JinaChat
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd
import openai
import subprocess
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, HuggingFaceHub
from langchain.chat_models import ChatOpenAI, ChatAnthropic
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

from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

os.environ['OPENAI_API_KEY'] = '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'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
'''
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
"""'''
# llm = OpenAI(model_name='text-davinci-001', temperature=0.3)
# agent = create_csv_agent(llm=llm, path='test.csv', verbose=False)
# memory = ConversationEntityMemory(llm=llm)
llm = HuggingFaceHub(repo_id="Open-Orca/OpenOrca",
                     model_kwargs={"temperature": 0.6, "max_length": 2000})
# llm = ChatAnthropic()
# new_memory = ConversationEntityMemory(llm=llm)
print(1)
conversation = LLMChain(llm=llm, prompt=prompt)
output = conversation.run("What is the Capital of england?")
print(output)
# onversation.add_agent(agent)

# print(conversation.prompt.template)

# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
'''llm = GPT4All(
    model=".\models\orca-mini-3b.ggmlv3.q4_0.bin")
llm_chain = LLMChain(prompt=prompt, llm=llm)

llm_chain.run("What do you mean by quantum computing?")'''
'''
while True:
    s = input("User: ")

    if s != 'exit':
        print(s)
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
'''
