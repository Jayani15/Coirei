from fastapi import FastAPI
from app.schemas import DebugRequest, DebugResponse
from app.agent import debug_agent

app = FastAPI(title="Debugging Assistant Agent")


@app.post("/debug", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    result = debug_agent(
        error_traceback=request.error_traceback,
        code_snippet=request.code_snippet
    )

    return result