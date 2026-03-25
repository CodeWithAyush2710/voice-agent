from fastapi import FastAPI, Request
from llm import detect_intent
from db import get_rate, save_order
from scheduler import schedule_followup
from utils import safe_response

app = FastAPI()

def followup_call(phone):
    print(f"Calling again to {phone}")
    # later integrate Vapi call API

@app.post("/handle-call")
async def handle_call(req: Request):
    data = await req.json()

    user_text = data.get("message", "")
    phone = data.get("phone", "")

    intent_data = detect_intent(user_text)

    intent = intent_data.get("intent")

    # 🟢 ORDER
    if intent == "order":
        product_code = intent_data.get("product_code")
        quantity = intent_data.get("quantity")

        rate = get_rate(product_code)

        if not rate:
            return {"response": "Product ka rate nahi mila"}

        amount = rate * quantity
        save_order(product_code, quantity, rate, amount)

        return {
            "response": f"Aapka order confirm ho gaya. Total {amount} rupaye."
        }

    # 🔵 RATE QUERY
    elif intent == "rate_query":
        product_code = intent_data.get("product_code")
        rate = get_rate(product_code)

        if not rate:
            return {"response": "Rate available nahi hai"}

        return {
            "response": f"Iska rate {rate} rupaye hai"
        }

    # 🟡 FOLLOW-UP
    elif intent == "follow_up":
        time_minutes = intent_data.get("time_minutes", 30)

        schedule_followup(followup_call, time_minutes, phone)

        return {
            "response": f"Theek hai, main {time_minutes} minute baad call karta hoon"
        }

    # 🔴 UNKNOWN
    else:
        return {
            "response": safe_response("Samajh nahi aaya, kya aap order dena chahte hain?")
        }