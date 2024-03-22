from openai import OpenAI
from dotenv import load_dotenv
import re
import os

load_dotenv(os.getenv("ENV_FILE", ".env"))


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

model = "gpt-3.5-turbo"

# Function to send a prompt to the OpenAI API and get a response
def query_openai(prompt_text):
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
  return regix_text(query_openai(prompt()))[0]


if __name__ == "__main__":
    print(get_response())