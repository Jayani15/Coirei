from pydantic import BaseModel


class DebugRequest(BaseModel):
    error_traceback: str
    code_snippet: str


class DebugResponse(BaseModel):
    explanation: str
    suggested_fix: str
    corrected_code: str
    confidence: float