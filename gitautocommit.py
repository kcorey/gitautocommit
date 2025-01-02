#! /usr/bin/env python3

import os
import random
import time
import subprocess
from datetime import datetime
import openai
import shlex

# Define the list of repositories
REPOSITORIES = [
    "/Users/kencorey/Developer/gitautocommit",
    "/Users/kencorey/Developer/ShortUrl"
    # Add more repository paths here
]

# Chance to create a new commit message
CHANCE_CREATE_NEW_COMMIT_MESSAGE = 0.2

# Function to execute shell commands
def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(command)}: {e.stderr.strip()}")
        print(f"Return code: {e.returncode}, Output: {e.stdout.strip()}")
        return None

# Function to return a viable commit message that makes sense for this repository
def get_commit_message(repo_path):
    api_key = os.getenv("OPENAI_API_KEY")

    # if the api-key isn't found or is an empty string, generate a random one ourselves.
    if not api_key:
        return generate_commit_message()

    # Initialize the OpenAI client
    client = openai.Client(api_key=api_key)

    try:
        # Use the new API method to create a chat completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates commit messages for git repositories."},
                {"role": "user", "content": f"Generate a brief commit message for the repository at {repo_path}. The message should sound technical, perhaps even a little cryptic, but definitely a comment a terse engineer would make. Refer to particular files and or particular modules. Swearing and the odd joke are okay."}
            ]
        )
        return response.choices[0].message.content.strip("'\"")
    except Exception as e:
        print(f"Error generating commit message with OpenAI: {e}")
        return generate_commit_message()

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
            content = content + " "  # Append a space
            f.seek(0)
            f.write(content)  # Write the content back to the file
            if content.count(' ') > 10:  # Check if there are more than 10 spaces
                f.seek(0)
                f.write(content[:1])  # Write only the first character
                f.truncate()  # Truncate the file to the current position

    # Commit the change
    commit_message = get_commit_message(repo_path)
    # Directly pass the commit message without using shlex.quote
    run_command(["git", "commit", "-am", commit_message], cwd=repo_path)

# Function to push changes
def push_changes(repo_path):
    run_command(["git", "push"], cwd=repo_path)

# Main function to perform the updates and pushes
def perform_updates():
    # 20% of the time, perform updates
    if random.random() < CHANCE_CREATE_NEW_COMMIT_MESSAGE:
        print("Performing updates")
        for repo in REPOSITORIES:
            # check to see if the directory exists
            if os.path.exists(repo):
                print(f"Processing repository: {repo}")
                update_file(repo)
                push_changes(repo)
    else:
        print("Skipping updates")

# Define the template statements
TEMPLATES = [
    "Nuked [one]. [expression of concern], [wish]. [Alternative solution].",
    "Scrapped [one]. [expression of regret], [hope]. [Attempt at justification].",
    "Yanked [one]. [grumble], [fantasy fix]. [Snarky workaround].",
    "Punted [one]. [panic], [dream]. [Unconvincing excuse].",
    "Axed [one]. [apology], [vague desire]. [Desperate plea for mercy].",
    "Added [one]. [expression of concern], [wish]. [Alternative solution].",
    "Inserted [one]. [expression of regret], [hope]. [Attempt at justification].",
    "Changed [one]. [grumble], [fantasy fix]. [Snarky workaround].",
    "Modified [one]. [panic], [dream]. [Unconvincing excuse].",
    "Updated [one]. [apology], [vague desire]. [Desperate plea for mercy]."
]

# Define the lists of options for each placeholder
one_options = [
    "3 lines", "the other file", "some comments", "dead code", "unused import",
    "logging spam", "mysterious TODO", "rogue print statement", "half-baked function", "redundant check"
]

expression_of_concern_options = [
    "This feels bad", "Not proud of this", "Uh, oops", "Honestly, I blame caffeine",
    "Might regret this later", "Definitely not ideal", "No promises this works",
    "Feels illegal but here we are", "Just vibing", "I’ll explain if asked"
]

wish_options = [
    "Hope this sticks", "Please don’t break", "Maybe it just works", "Let this be the last time",
    "Wish me luck", "Crossing fingers", "Nobody saw this", "Here’s hoping",
    "Just let it deploy", "We pray to the merge gods"
]

alternative_solution_options = [
    "Will write tests, maybe", "Could’ve added a hack but didn’t", "Revisit if on fire",
    "We’ll see in prod", "Future me can suffer", "More duct tape next time",
    "Will document eventually", "Slap some error handling", "Pretend it’s a feature",
    "Move fast, cry later"
]

# Define additional lists for other placeholders
expression_of_regret_options = [
    "Sorry about this", "My bad", "Oops", "Regrettably", "Apologies",
    "I didn't mean to", "This was unexpected", "I should have known better",
    "Not my finest moment", "I owe you one"
]

hope_options = [
    "Hope it works", "Fingers crossed", "Let's see what happens", "Here's hoping",
    "Maybe this time", "With any luck", "I hope for the best", "Let's pray",
    "Wish me luck", "I hope this sticks"
]

attempt_at_justification_options = [
    "It seemed like a good idea", "I had no choice", "It was necessary",
    "I promise it makes sense", "Trust me on this", "It was the only way",
    "I had to do it", "It was unavoidable", "I had to try", "It was worth a shot"
]

grumble_options = [
    "This is annoying", "I hate this", "Why me?", "Not again", "This is frustrating",
    "I can't believe this", "This is ridiculous", "Why does this happen?", "This is a pain", "I don't like this"
]

fantasy_fix_options = [
    "If only it were that easy", "In a perfect world", "If I had a magic wand",
    "If only I could", "In my dreams", "If I could just", "If it were up to me",
    "If I had my way", "If I could do anything", "If I could make it happen"
]

snarky_workaround_options = [
    "This should do it", "Let's see if this works", "This might work",
    "This should fix it", "This should help", "This should solve it",
    "This should be fine", "This should be okay", "This should be good", "This should be enough"
]

panic_options = [
    "Oh no", "What now?", "This is bad", "I'm in trouble", "This is a disaster",
    "This is a nightmare", "This is a mess", "This is chaos", "This is a problem", "This is a crisis"
]

dream_options = [
    "I wish", "If only", "In my dreams", "In a perfect world", "If I could",
    "If it were up to me", "If I had my way", "If I could do anything", "If I could make it happen", "If I could just"
]

unconvincing_excuse_options = [
    "I had no choice", "It was necessary", "I promise it makes sense",
    "Trust me on this", "It was the only way", "I had to do it",
    "It was unavoidable", "I had to try", "It was worth a shot", "It seemed like a good idea"
]

apology_options = [
    "Sorry about this", "My bad", "Oops", "Regrettably", "Apologies",
    "I didn't mean to", "This was unexpected", "I should have known better",
    "Not my finest moment", "I owe you one"
]

vague_desire_options = [
    "I hope this works", "I wish this would work", "I want this to work",
    "I need this to work", "I hope this is okay", "I wish this is okay",
    "I want this to be okay", "I need this to be okay", "I hope this is fine", "I wish this is fine"
]

desperate_plea_for_mercy_options = [
    "Please forgive me", "Please don't be mad", "Please don't hate me",
    "Please don't be angry", "Please don't be upset", "Please don't be disappointed",
    "Please don't be frustrated", "Please don't be annoyed", "Please don't be irritated", "Please don't be bothered"
]

def generate_commit_message():
    # Select a random template
    template = random.choice(TEMPLATES)
    
    # Replace placeholders with random choices from the respective lists
    message = template.replace("[one]", random.choice(one_options))
    message = message.replace("[expression of concern]", random.choice(expression_of_concern_options))
    message = message.replace("[wish]", random.choice(wish_options))
    message = message.replace("[Alternative solution]", random.choice(alternative_solution_options))
    message = message.replace("[expression of regret]", random.choice(expression_of_regret_options))
    message = message.replace("[hope]", random.choice(hope_options))
    message = message.replace("[Attempt at justification]", random.choice(attempt_at_justification_options))
    message = message.replace("[grumble]", random.choice(grumble_options))
    message = message.replace("[fantasy fix]", random.choice(fantasy_fix_options))
    message = message.replace("[Snarky workaround]", random.choice(snarky_workaround_options))
    message = message.replace("[panic]", random.choice(panic_options))
    message = message.replace("[dream]", random.choice(dream_options))
    message = message.replace("[Unconvincing excuse]", random.choice(unconvincing_excuse_options))
    message = message.replace("[apology]", random.choice(apology_options))
    message = message.replace("[vague desire]", random.choice(vague_desire_options))
    message = message.replace("[Desperate plea for mercy]", random.choice(desperate_plea_for_mercy_options))
    
    return message

if __name__ == "__main__":
    perform_updates()

