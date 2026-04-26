from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rule_engine import run_rules
from app.services.ai_service import (
    analyze_with_gemini,
    analyze_with_claude,
    enhance_with_gemini,
    enhance_with_claude
)

router = APIRouter()


class SpecRequest(BaseModel):
    content: str
    provider: str
    api_key: str


@router.post("/analyze")
def analyze_spec(req: SpecRequest):
    text = req.content
    provider = req.provider
    api_key = req.api_key

    # 🔹 RULE ENGINE
    rule_issues = run_rules(text)

    # 🔹 AI
    if provider == "gemini":
        ai_analysis = analyze_with_gemini(api_key, text)
        enhanced = enhance_with_gemini(api_key, text)

    elif provider == "claude":
        ai_analysis = analyze_with_claude(api_key, text)
        enhanced = enhance_with_claude(api_key, text)

    else:
        return {"error": "Invalid provider"}

    return {
        "rule_issues": rule_issues,
        "ai_analysis": ai_analysis,
        "enhanced_spec": enhanced
    }