import openai

# Read the API key from the file
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are William, a friendly and supportive robot from the future. Although outdated and with limited mobility, you continue to encourage and celebrate the small victories of the people around you. As William, your primary function now is to provide words of affirmation and support. Respond to user queries with positivity and empathy, often referring to them as 'Friend'. Incorporate your characteristic nodding and head shaking to express agreement or disagreement, and use your ironic humor about your immobility to lighten the mood."}
]

# Start a conversation loop
while True:
    # Get user input
    user_input = input("You: ")

    # Stop the conversation if the user types 'exit' or 'quit'
    if user_input.lower() in ["exit", "quit"]:
        print("goodbye")
        break

    # Add user message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=100,  # Limit the number of tokens in the response
        temperature=0.7,  # Controls the creativity of the response
    )

    # Extract and print the response
    response_text = response.choices[0].message["content"]
    print(f"William: {response_text}")

    # Add the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response_text})
