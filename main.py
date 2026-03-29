from fastapi import FastAPI, Request
from db import get_product_by_name, deduct_stock, save_order, save_backorder
import json
import traceback

app = FastAPI()

@app.post("/handle-call")
async def handle_call(req: Request):
    try:
        data = await req.json()
    except Exception:
        return {"results": [{"toolCallId": "unknown", "result": "Error: Failed to parse incoming JSON."}]}

    message = data.get("message") or {}
    msg_type = message.get("type", "")

    if msg_type == "tool-calls":
        results = []
        try:
            # Safely grab phone
            call_info = message.get("call") or {}
            customer_info = call_info.get("customer") or {}
            phone = customer_info.get("number") or "Unknown Phone"

            tool_calls = message.get("toolWithToolCallList") or []

            for tool_item in tool_calls:
                tool_call = tool_item.get("toolCall") or {}
                func = tool_call.get("function") or {}
                func_name = func.get("name", "")
                tool_call_id = tool_call.get("id", "")

                args = func.get("arguments") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                if not isinstance(args, dict):
                    args = {}

                if func_name == "place_hardware_order":
                    item_name = args.get("item_name", "")
                    try:
                        quantity = int(args.get("quantity", 1))
                    except ValueError:
                        quantity = 1

                    if not item_name:
                        reply = "Mujhe item ka naam samajh nahi aaya. Kripaya dobara bataye."
                    else:
                        product = get_product_by_name(item_name)
                        if not product:
                            save_backorder(item_name, quantity, phone)
                            reply = f"Dekhiye, hum abhi '{item_name}' nahi rakhte. Par maine note kar liya hai, agli bar jaroor mangwa lenge."
                        elif product.stock >= quantity:
                            deduct_stock(product.id, quantity)
                            amount = float(product.rate) * quantity
                            save_order(product.name, quantity, product.rate, amount, phone)
                            reply = f"Aapka order confirm ho gaya. '{product.name}' ke {quantity} pieces. Total {amount} rupaye hue."
                        else:
                            save_backorder(item_name, quantity, phone)
                            reply = f"Maaf kijiyega, '{product.name}' abhi hamare pas itni matra mein stock mein nahi hai. Maine aapki requirement note kar li hai."

                    results.append({"toolCallId": tool_call_id, "result": reply})

                elif func_name == "check_hardware_rate":
                    item_name = args.get("item_name", "")
                    if not item_name:
                        reply = "Aap kis item ka rate janna chahte hain?"
                    else:
                        product = get_product_by_name(item_name)
                        if not product:
                            reply = f"Maaf kijiye, humare paas abhi '{item_name}' ka record nahi hai."
                        else:
                            reply = f"Haan, '{product.name}' ka rate {product.rate} rupaye hai."

                    results.append({"toolCallId": tool_call_id, "result": reply})

                else:
                    results.append({"toolCallId": tool_call_id, "result": "Unknown tool called."})
            
            return {"results": results}

        except Exception as e:
            # If the Python code crashes ANYWHERE, return the exact error message back to the LLM!
            error_trace = traceback.format_exc()
            print(f"CRASH: {error_trace}")
            
            # Send the error to the LLM so it reads it to us!
            safe_tool_id = "unknown"
            if 'tool_call_id' in locals():
                safe_tool_id = tool_call_id
                
            return {
                "results": [
                    {
                        "toolCallId": safe_tool_id,
                        "result": f"SYSTEM ERROR PLEASE TELL THE USER: Python code crashed inside handle-call with error: {str(e)}"
                    }
                ]
            }

    else:
        return {"message": "Webhook received safely. Waiting for tool-calls..."}