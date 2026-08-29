import ollama

model = "qwen2.5:14b"

print("What are we working on today?\n\n")

conversation = []

while True:

    request = input("You:\n")
    
    if request == "exit":
        break

    conversation.append(
        {
        "role": "user",
        "content": request
        }
        )

    response = ollama.chat(model=model, messages=conversation)

    conversation.append(
        {
		"role": "assistant",
        "content": response.message.content
        }
        )

    print(f"\nScarlett:\n{response.message.content}\n")




