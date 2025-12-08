# GitHub Copilot Setup Guide

This guide will help you set up GitHub Copilot and enable the agent features in VS Code for this project.

## Prerequisites

1. **GitHub Student Developer Pack**: Make sure you have access to the [GitHub Student Developer Pack](https://education.github.com/pack)
2. **VS Code**: Install [Visual Studio Code](https://code.visualstudio.com/)
3. **GitHub Account**: Ensure you're signed in to GitHub with your student account

## Installation Steps

### Step 1: Install Required VS Code Extensions

Open VS Code and install the following extensions:

1. **GitHub Copilot** (`github.copilot`)
   - Open the Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "GitHub Copilot"
   - Click Install

2. **GitHub Copilot Chat** (`github.copilot-chat`)
   - Search for "GitHub Copilot Chat"
   - Click Install

Alternatively, VS Code will prompt you to install recommended extensions when you open this project.

### Step 2: Sign in to GitHub Copilot

1. After installing the extensions, click on the Accounts icon in the Activity Bar (bottom left)
2. Select "Sign in to GitHub to use GitHub Copilot"
3. Follow the authentication flow to sign in with your GitHub account
4. Authorize GitHub Copilot to access your account

### Step 3: Verify GitHub Copilot is Active

1. Look for the GitHub Copilot icon in the status bar (bottom right)
2. The icon should show that Copilot is active
3. If it shows an error, click on it to see details and troubleshoot

### Step 4: Enable and Access GitHub Copilot Agents

GitHub Copilot Agents (also called Chat Participants) are accessible through the Chat view:

1. **Open GitHub Copilot Chat**:
   - Click the Chat icon in the Activity Bar (left sidebar)
   - Or press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Alt+I` (Mac)
   - Or use Command Palette: `Ctrl+Shift+P` / `Cmd+Shift+P` and search for "GitHub Copilot: Open Chat"

2. **Use Agent Commands**:
   In the chat interface, you can use agents by typing `@` followed by the agent name:
   - `@workspace` - Ask questions about your workspace
   - `@vscode` - Get help with VS Code features
   - `@terminal` - Get help with terminal commands
   - `@github` - Search and ask questions about GitHub

3. **Slash Commands**:
   You can also use slash commands like:
   - `/explain` - Explain code
   - `/fix` - Fix code issues
   - `/tests` - Generate tests
   - `/new` - Create new code

### Step 5: Configure Settings (Already Done)

This project includes VS Code settings that enable GitHub Copilot features. The settings are in `.vscode/settings.json` and include:

- Copilot enabled for all file types
- Auto-completions enabled
- Chat participant detection enabled

## Troubleshooting

### Issue: "Agent option not visible in VS Code"

**Solution 1: Update VS Code and Extensions**
1. Update VS Code to the latest version (Help > Check for Updates)
2. Update GitHub Copilot extensions:
   - Open Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
   - Click the gear icon on GitHub Copilot
   - Select "Check for Updates"

**Solution 2: Verify GitHub Copilot Subscription**
1. Go to [GitHub Copilot Settings](https://github.com/settings/copilot)
2. Verify your subscription is active
3. If using Student Developer Pack, ensure it's still valid

**Solution 3: Check Extension Compatibility**
1. Ensure you're using VS Code version 1.75.0 or later
2. GitHub Copilot Chat requires specific VS Code versions
3. Update both VS Code and the extensions if needed

**Solution 4: Reload VS Code**
1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Developer: Reload Window"
3. Press Enter

**Solution 5: Check Settings**
1. Open Settings (Ctrl+, / Cmd+,)
2. Search for "github.copilot"
3. Ensure "GitHub Copilot: Enable" is checked for all languages
4. Search for "chat.experimental.detectParticipant"
5. Ensure it's enabled

**Solution 6: Sign Out and Sign In Again**
1. Click on the Accounts icon (bottom left)
2. Click on your GitHub account
3. Select "Sign Out"
4. Sign in again following Step 2 above

### Issue: "Copilot suggestions not appearing"

1. Check that Copilot is enabled in the status bar
2. Verify your GitHub Copilot subscription is active
3. Try disabling and re-enabling the extension
4. Check your internet connection

### Issue: "Chat view doesn't show agents"

1. Make sure you have the latest version of GitHub Copilot Chat extension
2. Enable the experimental feature: `"chat.experimental.detectParticipant.enabled": true`
3. Reload VS Code window

## Using GitHub Copilot in This Project

### For Python (Backend)
- Copilot will help with Flask routes, database models, and ML code
- Use `/explain` to understand complex algorithms
- Use `/tests` to generate unit tests

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
- [GitHub Student Developer Pack](https://education.github.com/pack)
- [VS Code GitHub Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

## Support

If you continue to experience issues:
1. Check the [GitHub Copilot Status Page](https://www.githubstatus.com/)
2. Visit [GitHub Copilot Community](https://github.community/c/copilot/44)
3. Contact GitHub Support through your Student Developer Pack portal
