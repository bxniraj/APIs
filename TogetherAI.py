from dotenv import load_dotenv
from openai import OpenAI
import re
import os

load_dotenv(os.getenv("ENV_FILE", ".env"))

client = OpenAI(
  api_key=os.environ["TOGETHERAI_API_KEY"], # ENTER YOUR API KEY HERE
  base_url='https://api.together.xyz/v1',
)

model = "Qwen/Qwen1.5-72B-Chat"

# Query the model with a prompt
def query_togetherai(prompt_text):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text},
        ]
    )
    # Assuming you want the last response from the model
    last_response = response.choices[0].message.content.strip()

    return last_response

# Remove \n and spaces from response
def regix_text(text):
  processed_response = re.sub(r'\n\n', '\n\n', text)
  processed_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', processed_response)
  sections = re.split(r'\n\n+', processed_text)
  return sections

def prompt():
  return "What is the capital of France?"

def get_response():
  return regix_text(query_togetherai(prompt()))[0]


if __name__ == "__main__":
    print(get_response())