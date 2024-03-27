from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import re
import os

load_dotenv(os.getenv("ENV_FILE", ".env"))

app = FastAPI()

client = OpenAI(
  api_key=os.environ["TOGETHERAI_API_KEY"], # ENTER YOUR API KEY HERE
  base_url='https://api.together.xyz/v1',
)

# Qwen/Qwen1.5-72B-Chat

class Prompt(BaseModel):
    prompt: str
    model: str


@app.post("/response")
def get_response(prompt: Prompt):
  # Query the model with a prompt
  def query_togetherai(prompt_text):
      response = client.chat.completions.create(
          model=prompt.model,
          messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": prompt_text},
          ]
      )
      #the last response from the model
      return response.choices[0].message.content.strip()

  # Remove \n and spaces from response
  def regix_text(text):
    processed_response = re.sub(r'\n\n', '\n\n', text)
    processed_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', processed_response)
    return re.split(r'\n\n+', processed_text)
  
  return regix_text(query_togetherai(prompt.prompt))[0]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)