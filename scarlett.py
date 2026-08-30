import os
import subprocess

import ollama


model = "qwen2.5:14b"

print("\nWelcome to Scarlett. What are we working on today?\n\n")

conversation = []

while True:

    request = input("You:\n")

    command_request = request.lower().strip()

    if command_request in ("exit", "close", "quit"):
        break

    elif command_request == "help":
        print("""\nScarlett commands:

        about - Learn about Scarlett and what she can do.

        help - Show this list of available commands.

        exit - Exit Scarlett and return to shell.\n""")
        continue

    elif command_request == "about":
        print("""\nAbout Scarlett:

        Scarlett is a linux-first development companion built to help new and learning developers work through real projects while developing their skills.

        The goal is to make Python, Git, Linux, and other development tools easier to learn by providing guidance directly from the terminal.

        Scarlett is in early development. More tools and capabilities will be added as the project grows.\n""")
        continue

    elif command_request == "status":
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
            local_commits  = subprocess.run(
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
                    print(f"{'Uncommitted Changes:':<24} {tree_check.stdout.strip()}")
                    print(f"{'Unpushed Commits:':<24} {local_commits.stdout.strip()}")
                    print(f"{'Remote Commits:':<24} {remote_commits.stdout.strip()}\n")



        else:
            print(f"\n{'Git Repository:':<24} No")
            print(f"{'Current Directory:':<24} {cwd}")

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




