"""
Test script for /handle-call endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

test_cases = [
    {
        "name": "📦 Order Test",
        "data": {
            "message": "A102 ke 50 bhej do",
            "phone": "9876543210"
        }
    },
    {
        "name": "💰 Rate Query Test",
        "data": {
            "message": "B205 ka rate kya hai",
            "phone": "9876543210"
        }
    },
    {
        "name": "📞 Follow-up Test",
        "data": {
            "message": "30 minute baad call karna",
            "phone": "9876543210"
        }
    },
    {
        "name": "❓ Unknown Test",
        "data": {
            "message": "Namaste",
            "phone": "9876543210"
        }
    }
]

print("🚀 Starting API Tests...\n")

for test in test_cases:
    print(f"▶️  {test['name']}")
    print(f"   Input: {json.dumps(test['data'], indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/handle-call", json=test['data'])
        result = response.json()
        print(f"   ✅ Response: {result['response']}\n")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Error: Cannot connect to server at {BASE_URL}")
        print("   Make sure the server is running with: uvicorn main:app --reload\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")

print("✨ Tests completed!")
