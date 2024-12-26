from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import anthropic

app = FastAPI()

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",

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