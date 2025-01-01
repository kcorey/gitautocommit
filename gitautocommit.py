#! /usr/bin/env python3

import os
import random
import time
import subprocess
from datetime import datetime
import openai

# Define the list of repositories
REPOSITORIES = [
    "/Users/kencorey/Developer/gitautocommit",
    "/Users/kencorey/Developer/ShortUrl"
    # Add more repository paths here
]

# Function to execute shell commands
def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(command)}: {e.stderr.strip()}")
        return None

# Function to return a viable commit message that makes sense for this repository
def get_commit_message(repo_path):
    # Initialize the OpenAI client
    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    # Use the new API method to create a chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates commit messages for git repositories."},
            {"role": "user", "content": f"Generate a brief commit message for the repository at {repo_path}. The message should sound technical, perhaps even a little cryptic, but definitely a comment a terse engineer would make. Refer to particular files and or particular modules. Swearing and the odd joke are okay."}
        ]
    )
    return response.choices[0].message.content

# Function to update the .UpdateStatus file
def update_file(repo_path):
    file_path = os.path.join(repo_path, ".UpdateStatus")

    if not os.path.exists(file_path):
        # Create and initialize the file if it doesn't exist
        with open(file_path, "w") as f:
            f.write(" ")
        run_command(["git", "add", ".UpdateStatus"], cwd=repo_path)
    else:
        # Update the file if it exists
        with open(file_path, "r+") as f:
            content = f.read()
            content = (content + " ")[:10]  # Append a space and truncate to 10 characters
            f.seek(0)
            f.write(content)
            f.truncate()

    print(get_commit_message(repo_path))
    # Commit the change
    run_command(["git", "commit", "-am", get_commit_message(repo_path)], cwd=repo_path)

# Function to push changes
def push_changes(repo_path):
    run_command(["git", "push"], cwd=repo_path)

# Main function to perform the updates and pushes
def perform_updates():
    # 20% of the time, perform updates
    if random.random() < 0.2:
        print("Performing updates")
        for repo in REPOSITORIES:
            # check to see if the directory exists
            if os.path.exists(repo):
                print(f"Processing repository: {repo}")
                update_file(repo)
                push_changes(repo)
    else:
        print("Skipping updates")

if __name__ == "__main__":
    perform_updates()

