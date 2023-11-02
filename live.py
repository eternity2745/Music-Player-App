from PIL import Image
import io
from io import BytesIO
import requests
import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


image_bytes = query({
    "inputs": "A bustling urban center of advanced technology and intergalactic commerce, with intricate details and vibrant colors, 8k, photorealistic",
})
# You can access the image with PIL.Image for example
print(image_bytes)
image = Image.open(BytesIO(image_bytes))
image.save('test.png')
