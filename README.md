# Automated Git Committer

This repository contains a Python script that automates Git commits to multiple repositories at random intervals throughout the day. The script modifies a file named `.UpdateStatus` in each repository, ensuring regular commit activity. This is useful for keeping repositories active or demonstrating activity for GitHub streaks.

## How It Works
- The script generates 1 to 5 commits at random times per day.
- If the `.UpdateStatus` file doesn't exist, the script creates it, adds a space, commits, and pushes the change.
- If the file exists, it appends a space. If the file exceeds 10 characters, it truncates it to maintain a maximum length of 10.

## Customization

### Modify the Repositories
Edit the `REPOSITORIES` list in the script to include the paths to your local repositories:
```python
REPOSITORIES = [
    "/path/to/repo1",
    "/path/to/repo2",
    # Add more paths here
]
```

### Adjust Commit Frequency
To change the number of commits per day, modify this line:
```python
num_commits = random.randint(1, 5)  # 1-5 commits per day
```
Adjust the range to suit your needs.

### Commit Message
The commit message format is:
```python
f"Update .UpdateStatus at {datetime.now()}"
```
You can modify this message to reflect different content.

## Running the Script Periodically

### Linux
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add the following line to run the script daily at 9 AM (adjust path and time as needed):
   ```bash
   0 9 * * * /usr/bin/python3 /path/to/script.py
   ```
3. Save and exit.

### macOS
1. Use `launchd` to run the script periodically.
2. Create a `plist` file in `~/Library/LaunchAgents/`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <plist version="1.0">
     <dict>
       <key>Label</key>
       <string>com.user.gitautocommit</string>
       <key>ProgramArguments</key>
       <array>
         <string>/usr/bin/python3</string>
         <string>/path/to/script.py</string>
       </array>
       <key>StartInterval</key>
       <integer>86400</integer>  <!-- Run every 24 hours -->
       <key>RunAtLoad</key>
       <true/>
     </dict>
   </plist>
   ```
3. Load the plist:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.user.gitautocommit.plist
   ```

### Windows
1. Open Task Scheduler.
2. Create a new task:
   - General Tab: Name it and choose "Run whether user is logged on or not".
   - Triggers Tab: Create a daily trigger.
   - Actions Tab: Select "Start a Program" and add:
     ```
     Program/script: python
     Add arguments: /path/to/script.py
     ```
3. Save the task and run it manually to test.

## Requirements
- Python 3
- Git installed and configured
- SSH keys set up for your GitHub account (if pushing to remote repositories)

## Troubleshooting
- Ensure Python is installed and available in your PATH.
- Verify the Git installation and repository paths are correct.
- Check repository permissions and SSH configurations.

---
Feel free to fork this repository and adapt it to your needs!

