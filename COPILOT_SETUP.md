# GitHub Copilot Setup Guide

This guide will help you set up GitHub Copilot and enable the agent features in VS Code for this project.

## Understanding GitHub Copilot Agents

**Important:** GitHub Copilot agents (like @workspace, @vscode, @terminal) are **not** separate menu options. They appear as suggestions when you type `@` in the GitHub Copilot Chat input box.

If you only see "Edit" and "Ask" buttons but no "Agent" option, that's normal! Agents are accessed by typing `@` in the chat input field.

## Prerequisites

1. **GitHub Student Developer Pack**: Make sure you have access to the [GitHub Student Developer Pack](https://education.github.com/pack)
2. **VS Code Version**: You need VS Code version **1.85.0 or later** for full agent support
3. **GitHub Account**: Ensure you're signed in to GitHub with your student account

## Installation Steps

### Step 1: Update VS Code (CRITICAL)

**GitHub Copilot agents require VS Code 1.85.0 or later!**

1. Open VS Code
2. Go to Help > About (or Code > About VS Code on Mac)
3. Check your version number
4. If it's older than 1.85.0, go to Help > Check for Updates
5. Download and install the latest version

### Step 2: Install Required VS Code Extensions

Open VS Code and install the following extensions:

1. **GitHub Copilot** (`github.copilot`)
   - Open the Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "GitHub Copilot"
   - Click Install

2. **GitHub Copilot Chat** (`github.copilot-chat`)
   - Search for "GitHub Copilot Chat"
   - Click Install
   - **Make sure to install the latest version!**

Alternatively, VS Code will prompt you to install recommended extensions when you open this project.

### Step 3: Sign in to GitHub Copilot

1. After installing the extensions, click on the Accounts icon in the Activity Bar (bottom left)
2. Select "Sign in to GitHub to use GitHub Copilot"
3. Follow the authentication flow to sign in with your GitHub account
4. Authorize GitHub Copilot to access your account

### Step 4: Verify GitHub Copilot is Active

1. Look for the GitHub Copilot icon in the status bar (bottom right)
2. The icon should show that Copilot is active
3. If it shows an error, click on it to see details and troubleshoot

### Step 5: How to Access and Use GitHub Copilot Agents

**This is where agents are located - not in a menu, but in the chat input!**

1. **Open GitHub Copilot Chat**:
   - Click the Chat icon in the Activity Bar (left sidebar) - it looks like a chat bubble
   - Or press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Alt+I` (Mac)
   - Or use Command Palette: `Ctrl+Shift+P` / `Cmd+Shift+P` and search for "GitHub Copilot Chat: Focus on Chat View"

2. **Access Agents by Typing `@`**:
   - In the chat input box at the bottom, type `@` (the @ symbol)
   - You should see a dropdown list of available agents:
     - `@workspace` - Ask questions about your workspace/codebase
     - `@vscode` - Get help with VS Code features
     - `@terminal` - Get help with terminal commands
     - `@github` - Search and ask questions about GitHub (if available)
   - Select an agent from the list or continue typing its name
   - Then type your question after the agent name

   **Example:** `@workspace where is the authentication logic?`

3. **Use Slash Commands** (without agents):
   You can also use slash commands in the chat:
   - `/explain` - Explain selected code
   - `/fix` - Fix problems in selected code
   - `/tests` - Generate tests
   - `/new` - Generate new code
   - `/clear` - Clear the chat

### Step 6: Configure Settings (Already Done)

This project includes VS Code settings that enable GitHub Copilot features. The settings are in `.vscode/settings.json` and include:

- Copilot enabled for all file types
- Auto-completions enabled
- Chat participant detection enabled

## Troubleshooting

### Issue: "I can only see Edit and Ask, not Agent"

**This is expected behavior!** GitHub Copilot doesn't have a separate "Agent" button or menu. 

**How agents actually work:**
1. Open the Chat panel (Chat icon in left sidebar)
2. In the chat input box (where you type your message), type `@`
3. A dropdown will appear showing available agents
4. Select an agent and type your question

**Visual Guide:**
- ❌ **Wrong:** Looking for an "Agent" button in menus
- ✅ **Correct:** Type `@` in the chat input box to see agents

### Issue: "No agents appear when I type @"

**Solution 1: Check VS Code Version**
- Agents require VS Code 1.85.0 or later
- Go to Help > About and check your version
- Update if necessary

**Solution 2: Update GitHub Copilot Chat Extension**
1. Open Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
2. Find "GitHub Copilot Chat"
3. If an update is available, click Update
4. After updating, reload VS Code (Command Palette > "Developer: Reload Window")

**Solution 3: Verify Your Subscription**
1. Go to [GitHub Copilot Settings](https://github.com/settings/copilot)
2. Verify your subscription is active
3. If using Student Developer Pack, ensure it's still valid
4. Make sure GitHub Copilot Individual or Business is enabled

**Solution 4: Enable Chat Participants**
1. Open VS Code Settings (Ctrl+, / Cmd+,)
2. Search for `chat.participant`
3. Ensure `Chat > Experimental: Detect Participant Enabled` is checked
4. This should already be set in this project's settings.json

**Solution 5: Reload VS Code Window**
1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Developer: Reload Window"
3. Press Enter
4. Try typing `@` in the chat again

**Solution 6: Sign Out and Sign In Again**
1. Click on the Accounts icon (bottom left)
2. Click on your GitHub account
3. Select "Sign Out"
4. Restart VS Code
5. Sign in again following Step 3 above

**Solution 7: Check Extension Installation**
1. Open Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
2. Make sure both extensions are installed and enabled:
   - GitHub Copilot (github.copilot)
   - GitHub Copilot Chat (github.copilot-chat)
3. Both should show "Enabled" and not have any error messages

### Issue: "Copilot suggestions not appearing"

1. Check that Copilot is enabled in the status bar
2. Verify your GitHub Copilot subscription is active
3. Try disabling and re-enabling the extension
4. Check your internet connection

### Issue: "Chat view doesn't show up"

1. Make sure GitHub Copilot Chat extension is installed
2. Look for the Chat icon in the Activity Bar (left sidebar)
3. If you don't see it, try: View > Open View > GitHub Copilot Chat
4. Or use Command Palette: "GitHub Copilot Chat: Focus on Chat View"

## Quick Reference: How to Use Agents

Once you have the Chat panel open:

1. **Type `@workspace`** followed by your question about the codebase
   - Example: `@workspace how does the authentication work?`
   - Example: `@workspace find all API endpoints`

2. **Type `@vscode`** for VS Code help
   - Example: `@vscode how do I debug Python code?`

3. **Type `@terminal`** for terminal/command help
   - Example: `@terminal how do I run Flask server?`

The key is: **agents are accessed by typing `@` in the chat input, not through menu buttons!**

## Using GitHub Copilot in This Project

### For Python (Backend)
- Copilot will help with Flask routes, database models, and ML code
- Use `/explain` to understand complex algorithms
- Use `/tests` to generate unit tests
- Use `@workspace` to ask about project structure

### For React (Frontend)
- Copilot will assist with React components and JSX
- Use `@workspace` to ask about component structure
- Get help with state management and hooks

### General Tips
- Use inline suggestions while typing (Tab to accept)
- Use Chat for complex questions about the codebase
- Use `@workspace` to ask about project-specific code
- Use `@terminal` for command-line help

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [GitHub Student Developer Pack](https://education.github.com/pack)
- [VS Code GitHub Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

## Support

If you continue to experience issues:
1. Check the [GitHub Copilot Status Page](https://www.githubstatus.com/)
2. Visit [GitHub Copilot Community](https://github.community/c/copilot/44)
3. Contact GitHub Support through your Student Developer Pack portal
