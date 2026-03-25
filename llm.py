import requests
from config import GROQ_API_KEY, BASE_URL

def detect_intent(user_text):
    prompt = f"""
Extract intent from user input.

Return JSON only.

Possible intents:
- order
- rate_query
- follow_up
- unknown

Examples:

Input: A102 ke 50 bhej do
Output: {{"intent":"order","product_code":"A102","quantity":50}}

Input: A102 ka rate kya hai
Output: {{"intent":"rate_query","product_code":"A102"}}

Input: 30 min baad call karna
Output: {{"intent":"follow_up","time_minutes":30}}

Input: {user_text}
"""

    response = requests.post(
        BASE_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
    )

    try:
        content = response.json()["choices"][0]["message"]["content"]
        return eval(content)  # simple parsing (later replace with json.loads safely)
    except:
        return {"intent": "unknown"}