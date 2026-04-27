import json
import re
import google.generativeai as genai
import anthropic


# ------------------ JSON EXTRACTOR ------------------

def extract_json(text: str):
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    cleaned = re.sub(r"```(?:json)?", "", text)
    cleaned = cleaned.replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    match = re.search(r"\{.*?\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    print("⚠️ JSON extraction failed:\n", text)
    return None


# ------------------ GEMINI ANALYSIS ------------------

def analyze_with_gemini(api_key: str, text: str):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are a senior software architect reviewing a product specification.

Return ONLY valid JSON:

{{
  "ambiguities": [],
  "missing_requirements": [],
  "edge_cases": [],
  "risks": [],
  "measurability_issues": [],
  "inconsistencies": [],
  "improvements": []
}}

Guidelines:
- Identify vague terms
- Identify missing constraints (limits, validation, failure handling)
- Identify edge cases (timeouts, invalid input, concurrency)
- Identify risks (scaling, security, performance)
- Identify non-measurable requirements
- Identify contradictions

Keep each point short and precise.

Spec:
{text}
"""

    for _ in range(3):  # retry
        response = model.generate_content(prompt)
        parsed = extract_json(response.text)

        if parsed:
            return parsed

    return {
        "error": "Failed to parse AI response",
        "raw": response.text
    }


# ------------------ CLAUDE ANALYSIS ------------------

def analyze_with_claude(api_key: str, text: str):
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
Return ONLY valid JSON:

{{
  "ambiguities": [],
  "missing_requirements": [],
  "improvements": []
}}

Spec:
{text}
"""

    for _ in range(3):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )

            text_output = response.content[0].text
            parsed = extract_json(text_output)

            if parsed:
                return parsed

        except Exception as e:
            print("Claude error:", e)

    return {
        "error": "Claude failed",
        "raw": text_output
    }


# ------------------ GEMINI ENHANCEMENT ------------------

def enhance_with_gemini(api_key: str, text: str):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are a senior software architect and technical specification reviewer.

Your task is to IMPROVE the given specification while PRESERVING its structure and completeness.

========================
STRICT RULES (IMPORTANT)
========================

1. Output ONLY the improved specification.
   - No explanations
   - No commentary
   - No bullet points about your changes
   - No reasoning

2. DO NOT summarize the spec.
   - Do NOT compress into a paragraph
   - Do NOT reduce length artificially

3. PRESERVE STRUCTURE:
   - Keep all original sections
   - Maintain headings (##, ###)
   - Maintain API formats, JSON blocks, tables, and lists

4. IMPROVE QUALITY:
   - Convert vague statements into precise, testable requirements
   - Add missing constraints where logically required
   - Fix inconsistencies in terminology
   - Clarify ambiguous behavior
   - Improve API definitions if present

5. ENHANCE COMPLETENESS:
   - If missing, add (only if relevant):
     - Authentication / Authorization
     - Error Handling
     - Edge Cases
     - Data Model clarity
     - Non-functional requirements

6. DO NOT INVENT UNRELATED FEATURES:
   - Do not add new product ideas
   - Do not change system scope

7. STYLE:
   - Must remain a professional technical specification
   - Must be structured, readable, and implementation-ready

========================
INPUT SPECIFICATION
========================

{text}
"""

    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()

            if result:
                return result

        except Exception as e:
            print("Gemini error:", e)

    return "Error: Failed to generate enhanced spec"


# ------------------ CLAUDE ENHANCEMENT ------------------

def enhance_with_claude(api_key: str, text: str):
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
You are a senior software architect and technical specification reviewer.

Your task is to IMPROVE the given specification while PRESERVING its structure and completeness.

========================
STRICT RULES (IMPORTANT)
========================

1. Output ONLY the improved specification.
   - No explanations
   - No commentary
   - No bullet points about your changes
   - No reasoning

2. DO NOT summarize the spec.
   - Do NOT compress into a paragraph
   - Do NOT reduce length artificially

3. PRESERVE STRUCTURE:
   - Keep all original sections
   - Maintain headings (##, ###)
   - Maintain API formats, JSON blocks, tables, and lists

4. IMPROVE QUALITY:
   - Convert vague statements into precise, testable requirements
   - Add missing constraints where logically required
   - Fix inconsistencies in terminology
   - Clarify ambiguous behavior
   - Improve API definitions if present

5. ENHANCE COMPLETENESS:
   - If missing, add (only if relevant):
     - Authentication / Authorization
     - Error Handling
     - Edge Cases
     - Data Model clarity
     - Non-functional requirements

6. DO NOT INVENT UNRELATED FEATURES:
   - Do not add new product ideas
   - Do not change system scope

7. STYLE:
   - Must remain a professional technical specification
   - Must be structured, readable, and implementation-ready

========================
INPUT SPECIFICATION
========================

{text}
"""

    for _ in range(3):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.content[0].text.strip()

            if result:
                return result

        except Exception as e:
            print("Claude error:", e)

    return "Error: Failed to generate enhanced spec"