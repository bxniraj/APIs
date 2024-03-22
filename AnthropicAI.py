from anthropic import Anthropic
from dotenv import load_dotenv
import os
import re

load_dotenv(os.getenv("ENV_FILE", ".env"))


client = Anthropic(api_key=os.environ["ANTHROPICAI_API_KEY"])

model = "claude-3-opus-20240229"

# Extract text from response
def extract_text(message):
    extracted_text = ""
    for content_block in message.content:
        if content_block.type == 'text':
            extracted_text += content_block.text + " "
    return extracted_text.strip()

def query_anthropicai(prompt_text):
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt_text},
        ]
    )
    # Assuming you want the last response from the model
    last_response = extract_text(response)

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
  return regix_text(query_anthropicai(prompt()))[0]


if __name__ == "__main__":
    print(get_response())