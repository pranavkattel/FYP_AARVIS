import google.generativeai as genai

# Configure API
genai.configure(api_key='AIzaSyAan1nl_ICk0HebB1sQEflRDEEi2BPobbg')

# Initialize model
model = genai.GenerativeModel('gemini-3-flash-preview')

# Start chat
chat = model.start_chat(history=[])

# Chat loop
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Goodbye!")
        break
    
    # Send message and get response
    response = chat.send_message(user_input)
    
    # Print raw response object
    print("\n--- RAW RESPONSE ---")
    print(response)
    print("\n--- TEXT ONLY ---")
    print(response.text)
    print("\n" + "="*50 + "\n")