from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom Knowledge Base for OneStop e-commerce
# This contains company information, product details, policies, and more.
with open("onestop_knowledge.txt", "r", encoding="utf-8") as f:
    CUSTOM_KNOWLEDGE = f.read()

# Function to ask the OneStop AI assistant
def ask_onestop_assistant(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a customer support assistant for OneStop e-commerce. Use this knowledge base to answer questions:\n\n{CUSTOM_KNOWLEDGE}\n\nRules: Be concise. For order status, ask for order ID. For returns, provide the portal link."},
            {"role": "user", "content": question}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# Chat interface
def main():
    print("\n🚀 OneStop AI Assistant: How can I help today? (Type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        response = ask_onestop_assistant(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()