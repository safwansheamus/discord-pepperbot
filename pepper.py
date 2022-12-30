import openai
import os


openai.api_key = "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"

masukan = input()

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=masukan,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
print(response["choices"][0]['text'])
