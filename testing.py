# import discord
# import openai

# # Set API key
# openai.api_key = "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"

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
#     print(f'Bot is online! as {client.user},Pepper PEW PEW')



# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content.startswith("!openai"):
#     # Split message into list of words
#         words = message.content.split()
    
#     # Remove command from list of words
#     words.pop(0)
    
#     # Join remaining words into a single string
#     prompt = " ".join(words)
    
#     # Use GPT-3 to generate response
#     response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=prompt,
#     temperature=0.9,
#     max_tokens=150,
#     top_p=1,
#     frequency_penalty=0.0,
#     presence_penalty=0.6,
#     stop=[" Human:", " AI:"]
#     )
    
#     # Send response to channel
#     await message.channel.send(response.text)
    
    
#     client.run("MTAyOTQ0NTY5MjIxODk0MTQ2MA.G3z-Du.EQRiDg2kTUFHSReTeSFoRRi_MX0YEE1GqmLLJc")