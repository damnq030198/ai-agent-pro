import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.factory import ModelFactory

def test_claude_connection():
    print("🚀 Testing Claude Connection with Cache...")
    try:
        # Initialize default model (Claude 3.5 Sonnet)
        model = ModelFactory.get_model()
        
        prompt = "Hello, tell me a short joke about AI agents."
        
        # Test 1: First call (Should be Cache Miss)
        print("\n--- Test 1: Calling API (Expect Delay) ---")
        response1 = model.generate(prompt)
        print(f"Response: {response1}")
        
        # Test 2: Second call (Should be Cache Hit)
        print("\n--- Test 2: Calling with Cache (Expect Instant) ---")
        response2 = model.generate(prompt)
        print(f"Response (cached): {response2}")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_claude_connection()
