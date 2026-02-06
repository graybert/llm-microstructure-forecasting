import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

resp = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Reply with exactly one short sentence."},
        {"role": "user", "content": "Say hello and confirm you can output a number like 0.73."},
    ],
    temperature=0,
)

print(resp.choices[0].message.content)
