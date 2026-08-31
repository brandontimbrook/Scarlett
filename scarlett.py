import os
import subprocess

import ollama
import json

model = "qwen2.5:14b"

def help_scarlett():
    print("""\nScarlett Commands:

    about - Learn about Scarlett and what she can do.

    help - Show this list of available commands.

    status - Show the current project and Git status.

    exit / close / quit - Exit Scarlett and return to shell.\n""")

def about_scarlett():
    print("""\nAbout Scarlett:

        Scarlett is a linux-first development companion built to help new and learning developers work through real projects while developing their skills.

        The goal is to make Python, Git, Linux, and other development tools easier to learn by providing guidance directly from the terminal.

        Scarlett is in early development. More tools and capabilities will be added as the project grows.\n""")

def git_status():
    cwd = os.getcwd()

    git_check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True
            )
    if git_check.returncode == 0:
        print(f"\n{'Git Repository:':<24} Yes")
        print(f"{'Current Directory:':<24} {cwd}")

        branch_check = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
                )
        tree_check = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
                )
        local_commits = subprocess.run(
                ["git", "rev-list", "--count", "@{u}..HEAD"],
                capture_output=True,
                text=True
                )
        remote_commits = subprocess.run(
                ["git", "rev-list", "--count", "HEAD..@{u}"],
                capture_output=True,
                text=True
                )
        if branch_check.returncode == 0:
            print(f"{'Git Branch:':<24} {branch_check.stdout.strip()}")

            if tree_check.stdout == "":
                print(f"{'Working Tree:':<24} Clean")
                print(f"{'Uncommitted Changes:':<24} 0")
                print(f"{'Unpushed Commits:':<24} {local_commits.stdout.strip()}")
                print(f"{'Remote Commits:':<24} {remote_commits.stdout.strip()}\n")

            elif tree_check.stdout != "":
                print(f"{'Working Tree:':<24} Modified")
                print(f"{'Uncommitted Changes:':<24} {tree_check.stdout.strip().splitlines()}")
                print(f"{'Unpushed Commits:':<24} {local_commits.stdout.strip()}")
                print(f"{'Remote Commits:':<24} {remote_commits.stdout.strip()}\n")

    else:
        print(f"\n{'Git Repository:':<24} No")
        print(f"{'Current Directory:':<24} {cwd}")

def web_search(query):
    results = []
    search = ollama.web_search(query)
    for result in search.results:
        results.append(
                {
                    "title": result.title,
                    "url": result.url,
                    "content": result.content
                    }
                )
    return results

print("\nScarlett:\nWelcome to Scarlett. What are we working on today?\n")

conversation = []

while True:

    request = input("You:\n")

    command_request = request.strip().lower()

    if command_request in ("exit", "quit", "close", "bye"):
        break

    elif command_request == "help":
        help_scarlett()
        continue

    elif command_request == "about":
        about_scarlett()
        continue

    elif command_request == "status":
        git_status()
        continue

    conversation.append(
            {
                "role": "user",
                "content": request
                }
            )

    response = ollama.chat(
            model=model,
            messages=conversation,
            tools=[web_search],
            stream=True
            )
    
    full_response = ""
    tool_request = None
    tool_message = None

    for chunk in response:
        if chunk.message.tool_calls:
            tool_request = chunk.message.tool_calls[0]
            tool_message = chunk.message
        else:
            full_response += chunk.message.content


    print("\nScarlett:")

    if tool_request:
        full_response = ""

        tool_name = tool_request.function.name
        query = tool_request.function.arguments["query"]

        web_results = web_search(query)
        json_web = json.dumps(web_results)

        conversation.append(
                tool_message
                )

        conversation.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json_web
                    }
                )

        web_response = ollama.chat(
                model=model,
                messages=conversation,
                stream=True
                )

        for web_chunk in web_response:
            web_chunk_piece = web_chunk.message.content
            print(web_chunk_piece, end="", flush=True)
            full_response += web_chunk_piece

    else:
        print(full_response, end="", flush=True)


    print("\n")

    conversation.append(
            {
                "role": "assistant",
                "content": full_response
                }
            )

