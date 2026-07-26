from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_agent

app = FastAPI()

class RepoRequest(BaseModel):
    repo_url: str

@app.post("/review")
async def review_repo(req: RepoRequest):
    result = run_agent(req.repo_url)
    return {
        "review": result
    }