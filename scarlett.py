import ollama

model = "qwen2.5:14b"

print("What are we working on today?\n\n")

conversation = []

while True:

    request = input("You:\n")
    
    if request == "exit":
        break

    elif request == "help":
        print("""\nScarlett commands:

        about - Learn about Scarlett and what she can do.

        help - Show this list of available commands.

        exit - Exit Scarlett and return to shell.\n""")
        continue
    elif request == "about":
        print("""\nAbout Scarlett:

        Scarlett is a linux-first development companion built to help new and learning developers work through real projects while developing their skills.

        The goal is to make Python, Git, Linux, and other development tools easier to learn by providing guidance directly from the terminal.

        Scarlett is in early development. More tools and capabilities will be added as the project grows.\n""")
        continue

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




