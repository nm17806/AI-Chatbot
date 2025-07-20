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
def ask_onestop_assistant(chat_history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0.3
    )
    return response.choices[0].message.content

# Chat interface
def main():
    print("\n🚀 OneStop AI Assistant: How can I help today? (Type 'exit' to quit)")
    chat_history = [
        {"role": "system", "content": f"You are a customer support assistant for OneStop e-commerce. Use this knowledge base to answer questions:\n\n{CUSTOM_KNOWLEDGE}\n\nRules: Be concise. For order status, ask for order ID. For returns, provide the portal link."}
    ]
    while True:
        user_input = input("\nYou: ")
        abandon_triggers = [
            "maybe later", "not buying now", "not ready", "will come back", 
            "i’ll come back", "change my mind", "leave the cart", 
            "don’t want to checkout", "buy later", "not sure yet"
        ]

        if any(trigger in user_input.lower() for trigger in abandon_triggers):
            print("\nAssistant: We noticed you might be leaving without checking out. Here's a 5% off code just for you: STAY5 💸")
            print("Use it at checkout to complete your purchase today. Let me know if you need help!")
            continue 

        if user_input.lower() in ['exit', 'quit']:
            break
        
        chat_history.append({"role": "user", "content": user_input})
        response = ask_onestop_assistant(chat_history)
        print(f"\nAssistant: {response}")
        chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
