import gradio as gr
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from PIL import Image
import io
import requests
import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import GPTNeoXForCausalLM
import os
from transformers import pipeline
import transformers
import time
import torch

os.environ['OPENAI_API_KEY'] = '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'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
'''
model = GPTNeoXForCausalLM.from_pretrained(
    "EleutherAI/pythia-70m-deduped",
    revision="step3000",
    cache_dir="./pythia-70m-deduped/step3000",
)

tokenizer = AutoTokenizer.from_pretrained(
    "EleutherAI/pythia-70m-deduped",
    revision="step3000",
    cache_dir="./pythia-70m-deduped/step3000",
)

inputs = tokenizer("Make a 5 line poem", return_tensors="pt")
tokens = model.generate(
    **inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=50)
# tokenizer.decode(tokens[0])
print(tokenizer.decode(tokens[0]))
'''
'''

tokenizer = AutoTokenizer.from_pretrained("deepparag/Aeona")
model = AutoModelWithLMHead.from_pretrained("deepparag/Aeona")
# Let's chat for 4 lines
for step in range(4):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(
        input(">> User:") + tokenizer.eos_token, return_tensors='pt')
    # print(new_user_input_ids)
    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat(
        [chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(
        bot_input_ids, max_length=200,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=4,
        do_sample=True,
        top_k=100,
        top_p=0.7,
        temperature=0.8
    )

    # pretty print last ouput tokens from bot
    print("Aeona: {}".format(tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
'''
# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xxl")

# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xxl")

# inputs = tokenizer("Make a 5 line poem", return_tensors="pt")
# tokens = model.generate(
#    **inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=50)
# tokenizer.decode(tokens[0])
# print(tokenizer.decode(tokens[0]))
'''
pipe = pipeline(model='google/flan-t5-xxl')
pipe("Who made google?") 
'''

'''
config = transformers.AutoConfig.from_pretrained(
    'mosaicml/mpt-7b-chat',
    trust_remote_code=True
)
config.update({"max_seq_len": 4096})
model = transformers.AutoModelForCausalLM.from_pretrained(
    'mosaicml/mpt-7b-chat',
    config=config,
    trust_remote_code=True,
)
'''
'''
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


image_bytes = query({
    "inputs": "A futuristic city of kerala in 5000",
})
# You can access the image with PIL.Image for example
image = Image.open(io.BytesIO(image_bytes))
image.save('images/generated.png')
print("Done")
'''

# import model class and tokenizer

# import model class and tokenizer

# download and setup the model and tokenizer
model_name = 'facebook/blenderbot-400M-distill'
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)


def func(message):
    inputs = tokenizer(message, return_tensors="pt")
    result = model.generate(
        **inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=4500)
    return tokenizer.decode(result[0])


x = func("Hey there what's your name?")
print(x)
