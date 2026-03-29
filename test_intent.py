"""
Test intent detection with regex fallback
"""
from llm import detect_intent, detect_intent_regex

test_inputs = [
    "A102 ke 50 bhej do",
    "B205 ka rate kya hai",
    "30 minute baad call karna",
    "Namaste",
]

print("🧪 Testing Intent Detection\n")

for user_input in test_inputs:
    print(f"Input: '{user_input}'")
    
    # Test regex fallback directly
    regex_result = detect_intent_regex(user_input)
    print(f"  Regex: {regex_result}")
    
    # Test full detection (with LLM + fallback)
    result = detect_intent(user_input)
    print(f"  Final: {result}")
    print()
