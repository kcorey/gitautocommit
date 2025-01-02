# Automated Git Committer

This repository contains a Python script that automates Git commits to multiple repositories throughout the day. The script modifies a file named `.UpdateStatus` in each repository, ensuring regular commit activity. This is useful for keeping repositories active or demonstrating activity for GitHub streaks.

## Prerequisites

To use this script, you must have the following:

- A GitHub account  
- SSH keys set up for your GitHub account, allowing command-line access to your repositories.  
- A repo that you want to commit to  
- The repo cloned to a local directory

If you have not set up SSH keys yet, you can follow GitHub's official guide to generate and configure them: [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). Additionally, you need to add the SSH key to your GitHub account by following these steps: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

## How It Works

- The script has a percentage chance to generate commits each time that it runs.  
- If the `.UpdateStatus` file doesn't exist for a project, the script creates it, adds a space, commits, and pushes the change.  
- If the file exists, it appends a space. If the file exceeds 10 characters, it truncates it to maintain a maximum length of 10\.  Don't want any bloat, here.

## Customization

### Modify the Repositories

Edit the `REPOSITORIES` list in the script to include the paths to your local repositories:

REPOSITORIES \= \[

    "/path/to/repo1",

    "/path/to/repo2",

    \# Add more paths here

\]

### Adjust Commit Frequency

To change the number of commits per day, modify this line:

CHANCE\_CREATE\_NEW\_COMMIT\_MESSAGE \= 0.2

Which is a 20% chance that the new commits are created.

### Commit Message

The commit message will be automatically created.  There's a built-in random commit message generator that creates lines like:

- Yanked 3 lines. Why me?, If only I could. This should be okay.  
- Inserted the other file. Apologies, I hope for the best. I had no choice.

If you set `OPENAI_API_KEY` to a key from this page: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys), then you can get better AI generated messages (because we all need more AI random text, amirite?)  NOTE: this incurs a charge\!  You are responsible for any charges created.

## Running the Script Periodically

### Linux

1. Open the crontab editor:  
     
   crontab \-e  
     
2. Add the following line to run the script daily at 9 AM (adjust path and time as needed):  
     
   0 9 \* \* \* /usr/bin/python3 /path/to/script.py  
     
3. Save and exit.

### macOS

1. Use `launchd` to run the script periodically.  
2. Create a `plist` file in `~/Library/LaunchAgents/`:  
     
   \<?xml version="1.0" encoding="UTF-8"?\>  
     
   \<plist version="1.0"\>  
     
     \<dict\>  
     
       \<key\>Label\</key\>  
     
       \<string\>com.user.gitautocommit\</string\>  
     
       \<key\>ProgramArguments\</key\>  
     
       \<array\>  
     
         \<string\>/usr/bin/python3\</string\>  
     
         \<string\>/path/to/script.py\</string\>  
     
       \</array\>  
     
       \<key\>StartInterval\</key\>  
     
       \<integer\>86400\</integer\>  \<\!-- Run every 24 hours \--\>  
     
       \<key\>RunAtLoad\</key\>  
     
       \<true/\>  
     
     \</dict\>  
     
   \</plist\>  
     
3. Load the plist:  
     
   launchctl load \~/Library/LaunchAgents/com.user.gitautocommit.plist

### Windows

1. Open Task Scheduler.  
2. Create a new task:  
   - General Tab: Name it and choose "Run whether user is logged on or not".  
   - Triggers Tab: Create a daily trigger.  
   - Actions Tab: Select "Start a Program" and add:  
       
     Program/script: python  
       
     Add arguments: /path/to/script.py

     
3. Save the task and run it manually to test.

## Setting Up a Virtual Environment (venv)

For a safer and isolated Python environment, use `venv` to manage dependencies.

1. Create a virtual environment:  
     
   python \-m venv venv  
     
2. Activate the virtual environment:  
   - **Linux/macOS:**  
       
     source venv/bin/activate  
       
   - **Windows:**  
       
     venv\\Scripts\\activate

     
3. Install dependencies (if applicable):  
     
   pip install \-r requirements.txt  
     
4. Run the script within the virtual environment:  
     
   python /path/to/script.py

To deactivate the virtual environment:

 deactivate

## Requirements

- Python 3  
- Git installed and configured  
- SSH keys set up for your GitHub account (if pushing to remote repositories)

## Troubleshooting

- Ensure Python is installed and available in your PATH.  
- Verify the Git installation and repository paths are correct.  
- Check repository permissions and SSH configurations.

---

Feel free to fork this repository and adapt it to your needs\!
