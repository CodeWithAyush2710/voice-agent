import requests
import json
import re
from config import GROQ_API_KEY, BASE_URL

def clean_json(text):
    """
    Extract JSON from messy LLM output with multiple fallback strategies
    """
    text = text.strip()
    
    # Remove markdown code blocks if present
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    text = text.strip()
    
    try:
        # Try to find JSON object
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if match:
            json_str = match.group(0)
            # Validate it's proper JSON
            return json.loads(json_str)
    except:
        pass
    
    return None


def detect_intent_regex(user_text):
    """
    Fallback regex-based intent detection for Hindi inputs
    """
    text_lower = user_text.lower().strip()
    text_original = user_text.strip()
    
    # ORDER patterns: "50 kilo cement bhej do", "10 packet nail chahiye"
    # Basic numeric extraction and string split fallback. 
    # This is a very basic fallback for demonstration.
    order_match = re.search(r'(\d+)\s*(kilo|packet|piece|pc|pcs)?\s*([a-zA-Z\s]+?)\s*(bhej|dena|chahiye|order|do)', text_lower)
    if order_match:
        quantity = int(order_match.group(1))
        item_name = order_match.group(3).strip()
        if item_name:
             return {
                 "intent": "order",
                 "item_name": item_name,
                 "quantity": quantity
             }
    
    # RATE QUERY patterns: "cement ka rate", "nails ki kimat"
    if any(word in text_lower for word in ['rate', 'kimat', 'price', 'bhav']):
        rate_pattern = r'([a-zA-Z\s]+)\s+(ka|ki)\s+(rate|kimat|price|bhav)'
        match = re.search(rate_pattern, text_lower)
        if match:
            return {
                "intent": "rate_query",
                "item_name": match.group(1).strip()
            }
    
    # FOLLOW-UP patterns: "30 minute baad", "1 ghante mein", "2 hours baad call"
    followup_pattern = r'(\d+)\s+(?:minute|min|ghante|hour|hours?)'
    match = re.search(followup_pattern, text_lower)
    if match and any(word in text_lower for word in ['baad', 'mein', 'call', 'karna']):
        time_str = match.group(1)
        time_minutes = int(time_str)
        # If it's in hours, convert to minutes
        if 'ghante' in text_lower or 'hour' in text_lower:
            time_minutes = time_minutes * 60
        return {
            "intent": "follow_up",
            "time_minutes": time_minutes
        }
    
    return {"intent": "unknown"}


def detect_intent(user_text):
    prompt = f"""Extract intent and data from this Hindi/English input for a hardware shop. Output ONLY valid JSON.

Rules:
1. Output ONLY JSON object, nothing else
2. Always include "intent" key
3. No markdown formatting
4. Valid intents: order, rate_query, follow_up, unknown

JSON Format Examples:
{{"intent":"order","item_name":"Cement","quantity":50}}
{{"intent":"rate_query","item_name":"Nails 2 inch"}}
{{"intent":"follow_up","time_minutes":30}}
{{"intent":"unknown"}}

Hindi Input Patterns:
- Order: "50 bori cement bhej do" → item_name and quantity
- Order: "hammer chahiye 2 piece" → item_name and quantity
- Rate: "Nails ka rate kya hai" → item_name only
- Followup: "30 minute baad call karna" → time_minutes only

User Input: {user_text}
JSON Output:"""

    try:
        response = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 150
            },
            timeout=10
        )
        
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        print(f"🔥 LLM RAW: {content}")

        # Try to parse JSON
        result = clean_json(content)
        if result and isinstance(result, dict):
            print(f"✅ LLM PARSED: {result}")
            return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API ERROR: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON ERROR: {e}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # FALLBACK: Use regex-based detection
    print(f"⚡ FALLBACK: Using regex detection for '{user_text}'")
    fallback_result = detect_intent_regex(user_text)
    print(f"✅ REGEX RESULT: {fallback_result}")
    return fallback_result