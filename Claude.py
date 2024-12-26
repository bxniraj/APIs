from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import anthropic

app = FastAPI()

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="",

)

class Prompt(BaseModel):
    prompt: str
    
@app.post("/response")
def get_response(prompt: Prompt):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )
    return message.content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)