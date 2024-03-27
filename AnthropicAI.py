from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import re

load_dotenv(os.getenv("ENV_FILE", ".env"))

app = FastAPI()

client = Anthropic(api_key=os.environ["ANTHROPICAI_API_KEY"])

# claude-3-opus-20240229

class Prompt(BaseModel):
    prompt: str
    model: str


@app.post("/response")
def get_response(prompt: Prompt):
  # Extract text from response
  def extract_text(message):
      extracted_text = ""
      for content_block in message.content:
          if content_block.type == 'text':
              extracted_text += content_block.text + " "
      return extracted_text.strip()

  def query_anthropicai(prompt_text):
      response = client.messages.create(
          model=prompt.model,
          max_tokens=1024,
          messages=[
              {"role": "user", "content": prompt_text},
          ]
      )
      return extract_text(response)

  # Remove \n and spaces from response
  def regix_text(text):
    processed_response = re.sub(r'\n\n', '\n\n', text)
    processed_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', processed_response)
    sections = re.split(r'\n\n+', processed_text)
    return sections
  
  return regix_text(query_anthropicai(prompt.prompt))[0]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)