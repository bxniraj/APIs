from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import re
import os

load_dotenv(os.getenv("ENV_FILE", ".env"))

app = FastAPI()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]) # ENTER YOUR API KEY HERE

# gpt-3.5-turbo

class Prompt(BaseModel):
    prompt: str
    model: str


@app.post("/response")
def get_response(prompt: Prompt):
    # Function to send a prompt to the OpenAI API and get a response
    def query_openai(prompt_text):
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

    return regix_text(query_openai(prompt.prompt))[0]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
